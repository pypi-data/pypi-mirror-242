from logging import Logger
from statistics import mean
from typing import Optional
from datetime import datetime, timedelta
import sys
import uuid
import pytz


from Databases.Oracle.OracleClient import OracleClient

from Services.ServicesChecker import ServicesChecker
from Services.DBS.DBSWriter import DBSWriter
from Services.DBS.DBSReader import DBSReader
from Services.McM.McMClient import McMClient
from Services.ReqMgr.ReqMgrReader import ReqMgrReader
from Services.ReqMgr.ReqMgrWriter import ReqMgrWriter
from Services.Rucio.RucioReader import RucioReader
from Services.WorkQueue.WorkQueueReader import WorkQueueReader
from Utilities.WebTools import getResponse
from Utilities.Logging import getLogger, send_log_to_opensearch
from WorkflowMgmt.WorkflowController import WorkflowController
from WorkflowMgmt.WorkflowStatusEnforcer import WorkflowStatusEnforcer
from MongoControllers.RMController import RunningMonitorController
from MongoControllers.ForceCompletionController import ForceCompletionController
from MongoControllers.CampaignController import CampaignController
from Utilities.ConfigurationHandler import ConfigurationHandler


class RunningMonitor(OracleClient):
    """
    __RunningMonitor__
    General API for monitoring workflows in running open.
    """

    def __init__(self, logger: Optional[Logger] = None, **kwargs) -> None:
        try:
            super().__init__(self)
            self.logger = logger or getLogger(self.__class__.__name__)

            self.wqe_reader = WorkQueueReader()
            self.rucio_reader = RucioReader()
            self.reqmgr_reader = ReqMgrReader()
            self.campaign_controller = CampaignController()
            self.running_monitor_mongo = RunningMonitorController()
            self.force_completion_controller = ForceCompletionController()


            self.reqmgr_writer = ReqMgrWriter()

            self.dbs = {"writer": DBSWriter(), "reader": DBSReader()}

            self.workflows_to_force_complete = []

            self.run_id = uuid.uuid4().hex

            self.logger.info(f"Running Monitor run id :: {self.run_id}")
            self.logMsg = {
                "autoMsg": "\n This is an automated message",
            }

            unified_config = ConfigurationHandler("config/unifiedConfiguration.json")
            thresholds = unified_config.get("running_monitor_config")
            self.threshold_in_days_for_wf_in_running_open = thresholds.get("threshold_in_days_for_wf_in_running_open")
            self.threshold_in_days_for_wqe_in_acquired_or_available = thresholds.get("threshold_in_days_for_wqe_in_acquired_or_available")

            # self.thresholds = unified_config.get("running_monitor_config")

        except Exception as error:
            raise Exception(f"Error initializing Running Monitor\n{str(error)}")

    def go(self) -> bool:
        """
        The function to check if the running-monitor can go
        :return: True if it can go, False o/w
        """
        try:
            servicesChecker = ServicesChecker(softServices=["wtc", "jira"])
            return servicesChecker.check()

        except Exception as error:
            self.logger.error("Failed to check if Invalidator can go")
            self.logger.error(str(error))

    def _get_formatted_time_from_epoch(self, epoch_time):
        return self._get_time_from_epoch(epoch_time).strftime('%Y-%m-%d %H:%M:%S')

    def _get_time_from_epoch(self, epoch_time):
        return datetime.utcfromtimestamp(epoch_time)

    def get_transfer_status(self, wf_name):
        reqmgr_url = 'cmsweb.cern.ch'
        response = getResponse(
            reqmgr_url, f"/ms-transferor/data/info?request={wf_name}", headers={"Accept": "application/json"})
        data = response.get('result')
        all_transfers = [max(t['completion'])
                         for t in data[0].get('transferDoc')['transfers']]
        all_datasets = [t['dataset']
                        for t in data[0].get('transferDoc')['transfers']]
        return all_datasets, all_transfers

    def get_rucio_rules(self, dataset_name):
        return self.rucio_reader.rucio.list_did_rules(scope='cms', name=dataset_name)

    def run(self) -> None:
        """
        The function to run Running Open Monitor
        """
        try:
            stuck_wf_reports = []
            wfs = self.reqmgr_reader.getWorkflowsByStatus('running-open', details=True)
            self.logger.info(f"Running Monitoring is running. total running-open workflows: {len(wfs)}")
            for wf_json in wfs:
                wf_name = wf_json.get('_id')
                self.logger.info(f"Checking workflow {wf_name}")    
                datasets, transfer_stats = self.get_transfer_status(wf_name)
                incomplete_transfers = [transfer_stat for transfer_stat in transfer_stats if transfer_stat < 100]
                for transfer_stat in incomplete_transfers:
                
                    wf_controller = WorkflowController(wf_name, noSpec=True)
                    time_difference = self._get_time_difference_since_current_state(wf_json)

                    # Check if the last_update_time is older than threshold defined in UnifiedConfiguration
                    if time_difference > timedelta(days=self.threshold_in_days_for_wf_in_running_open):
                        self.logger.info(f"Workflow {wf_name} has been running-open since more than {self.threshold_in_days_for_wf_in_running_open} days, transfer stuck at {transfer_stat}")
                        eligibile_to_force_complete, any_wqe_stuck, wf_processed_data = self.process_stuck_wf(wf_controller, wf_json)
                        wf_processed_data['ms_transferor_percent'] = round(transfer_stat, 2)


                        if eligibile_to_force_complete:
                            self.logger.info(f"Workflow {wf_name} is eligible for force completion with completion {wf_processed_data['completion_percent']}")
                            self.workflows_to_force_complete.append(wf_processed_data)
                        
                        elif any_wqe_stuck:
                            self.logger.info(f"Workflow {wf_name} has stuck wqes and rucio rules :: {wf_processed_data['stuck_wqes']} :: {wf_processed_data['stuck_rucio_rules']}")
                            stuck_wf_reports.append(wf_processed_data)

                       
        
            self.logger.info(f"Running Monitoring is finished. total stuck transfers: {len(stuck_wf_reports)}",  )
            self._dump_stuck_transfers_in_mongo(stuck_wf_reports)
            self.logger.info(f"Stuck transfers total :: {len(stuck_wf_reports)} are dumped in mongo")

            self._force_complete_workflows()            

            self.logger.info("Notifications are complete, halting")

        except Exception as error:
            self.logger.error("Failed to run Running Monitor")
            self.logger.error(str(error))
            import traceback
            self.logger.error(traceback.format_exc())


    def _get_wfs_last_transition(self, wf_json):
        return wf_json['RequestTransition'][-1]['UpdateTime']

    def _is_eligible_for_force_completion(self, wf_json, completion):
        campaign_threshold = self._get_campaign_threshold_for_wf(wf_json)
        all_outputs_above_threshold = [ stat >= float(campaign_threshold) for stat in  completion.values()]
        self.logger.info(f"all_outputs_above_threshold :: {all_outputs_above_threshold} campaign_threshold :: {campaign_threshold}")
        return all(all_outputs_above_threshold), campaign_threshold

    def _get_campaign_threshold_for_wf(self, wf_json):
        campaign_name = wf_json.get('Campaign')
        campaign_threshold = self.campaign_controller.getCampaignValue(campaign_name, 'fractionpass', 1)
        return campaign_threshold
    
    def process_stuck_wf(self, wf_controller, wf_json, ):
        wf_name = wf_controller.wf
        competion_per_dataset = wf_controller.getCompletionFraction()
        mean_completion_percentage = mean(list(competion_per_dataset.values()))

        can_be_force_completed, campaign_threshold = self._is_eligible_for_force_completion(wf_json, competion_per_dataset)
        
        wf_report_data = {
                "wf_name": wf_name,
                "wf_data": wf_json,
                "prep_id": wf_json.get('PrepID'),
                "completion_percent": mean_completion_percentage,
                "completion_per_dataset": competion_per_dataset,
                "campaign_threshold": campaign_threshold,
                "running_open_since": self._get_formatted_time_from_epoch(self._get_wfs_last_transition(wf_json)),
                "run_id": self.run_id,
            }
        
        self.logger.info(f"completion datasets for {wf_name} :: {competion_per_dataset}, Overall completion :: {mean_completion_percentage}")
        
        fwqes = self._get_acquired_or_available_wqes(wf_name)
        any_wqe_stuck, stuck_wqes, stuck_rucio_rules = self._get_stuck_wqes_and_rucio_rules(fwqes)
        wf_report_data['stuck_wqes'] = stuck_wqes
        wf_report_data['stuck_rucio_rules'] = stuck_rucio_rules

        return can_be_force_completed, any_wqe_stuck, wf_report_data

    def _get_stuck_wqes_and_rucio_rules(self, fwqes):
        any_wqe_stuck = False
        stuck_wqes= []
        stuck_rucio_rules= []
        for wqe in fwqes:
            wqe_last_updated = datetime.now() - self._get_time_from_epoch(wqe['UpdateTime'])
            self.logger.info("wqe_last_updated.days ", wqe_last_updated.days)
            if wqe_last_updated.days > self.threshold_in_days_for_wqe_in_acquired_or_available:
                any_wqe_stuck = True
                # add wqe id
                self.logger.info(f"\t\t wqe has been stuck since more than {self.threshold_in_days_for_wqe_in_acquired_or_available} days :: ")
                self.logger.info(f" \t\t EventsWritten: {wqe['EventsWritten']}, FilesProcessed: {wqe['FilesProcessed']},\
                        PercentComplete: {wqe['PercentComplete']}, PercentSuccess: {wqe['PercentSuccess']}")
                input_blocks = list(wqe['Inputs'].keys())
                stuck_wqes.append(wqe)
                stuck_rucio_rules.extend(self._get_stuck_rucio_rules(input_blocks))
        return any_wqe_stuck,stuck_wqes,stuck_rucio_rules

    def _get_acquired_or_available_wqes(self, wf_name):
        wqes = self.wqe_reader.getWorkQueue(wf_name)
 
        wqes = [{**wqe.get('WMCore.WorkQueue.DataStructs.WorkQueueElement.WorkQueueElement'),
                'UpdateTime': wqe.get("updatetime")} for wqe in wqes]
        fwqes = [wqe for wqe in wqes if wqe.get('Status') in ['Acquired', 'Available']]
        return fwqes

    def _get_stuck_rucio_rules(self, input_blocks):
        stuck_rules = []
        rucio_rules_for_each_block = [self.get_rucio_rules(input_block) for input_block in input_blocks]
        for rucio_rules in rucio_rules_for_each_block:
            for rule in rucio_rules:
                stuck_rules.append({
                        'rule_id': rule['id'],
                        **rule
                })
        return stuck_rules

    def _get_time_difference_since_current_state(self, wf_json):
        wf_last_updated = self._get_time_from_epoch(self._get_wfs_last_transition(wf_json))
        return datetime.now() - wf_last_updated

    def _dump_stuck_transfers_in_mongo(self, reports):
        self.logger.info("Dumping stuck transfers in mongo. Clearing the collection first")

        output = self.running_monitor_mongo.clear()

        self.logger.info(f"collection cleared. output ::{output}")
        self.logger.info("Inserting stuck transfers in mongo")
        for report_data in reports:
            self.running_monitor_mongo.insert({**report_data, 
                                               "insertion_time": self._get_formatted_time_from_epoch(datetime.now().timestamp()),
                                               })

    def _force_complete_workflows(self):
        for wf_processed_data in self.workflows_to_force_complete:
            
            # TODO - Make it configurable
            try:
                self.logger.info(f"force completing workflow {wf_processed_data['wf_name']} with completion {wf_processed_data['completion_percent']}")
                self.reqmgr_writer.forceCompleteWorkflow(wf_processed_data['wf_name'])
                self.log_force_completion_to_opensearch(wf_processed_data)
                self._insert_force_completed_wf_to_mongo(wf_processed_data)
                self.logger.info(f"workflow {wf_processed_data['wf_name']} force completed")
            except Exception as ex:
                self.logger.error(f"force completing workflow {wf_processed_data['wf_name']} failed with exception {ex}")

    def log_force_completion_to_opensearch(self, wf_processed_data):
        log_msg = f"\n \
                Force Completed workflow {wf_processed_data['wf_name']} \n \
                with prepId {wf_processed_data['prep_id']} \n with completion percentage {wf_processed_data['completion_percent']} \
                and campaign threshold {wf_processed_data['campaign_threshold']}\n \
                completion per dataset \n {wf_processed_data['completion_per_dataset']} \n\n\
                run_id of the running monitor {self.run_id}"
                        
        send_log_to_opensearch("running-monitor", log_msg, wf_processed_data, level = 'workflow')
            

    def _insert_force_completed_wf_to_mongo(self, wf_data):
        self.logger.info(f"Inserting force completed workflow {wf_data['wf_name']} to mongo")
        timezone = pytz.timezone('Europe/Zurich')
        self.force_completion_controller.insert({
                **wf_data,
                "insertion_time": self._get_formatted_time_from_epoch(datetime.now(timezone).timestamp()),
            }, {"wf_name": wf_data['wf_name']})
        self.logger.info(f"Inserted force completed workflow {wf_data['wf_name']} to mongo")


if __name__ == "__main__":
    running_monitor = RunningMonitor()
    if running_monitor.go():
        running_monitor.run()
