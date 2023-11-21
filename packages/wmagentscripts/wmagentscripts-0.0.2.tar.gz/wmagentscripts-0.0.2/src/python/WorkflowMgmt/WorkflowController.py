import os
import json
import math
from logging import Logger
from collections import defaultdict
from time import mktime, gmtime

from Databases.Oracle.OracleClient import OracleClient
from Databases.Oracle.OracleDB import Workflow as OracleWorkflow

from MongoControllers.CampaignController import CampaignController

from WorkflowMgmt.SiteController import SiteController
from WorkflowMgmt.WorkflowSchemaHandlers.BaseWfSchemaHandler import BaseWfSchemaHandler
from WorkflowMgmt.WorkflowSchemaHandlers.StepChainWfSchemaHandler import StepChainWfSchemaHandler
from WorkflowMgmt.WorkflowSchemaHandlers.TaskChainWfSchemaHandler import TaskChainWfSchemaHandler
from WorkflowMgmt.CacheableBase import CacheableBase,cached_json

from Services.ReqMgr.ReqMgrReader import ReqMgrReader
from Services.DBS.DBSReader import DBSReader
from Services.Rucio.RucioReader import RucioReader
from Services.WMStats.WMStatsReader import WMStatsReader
from Services.WorkQueue.WorkQueueReader import WorkQueueReader
from Services.ACDC.ACDCReader import ACDCReader
from Services.GWMSMon.GWMSMonReader import GWMSMonReader

from Utilities.ConfigurationHandler import ConfigurationHandler
from Utilities.IteratorTools import mapValues
from Utilities import DataTools
from Utilities.Logging import getLogger

from typing import Optional, Tuple, List, Union


class WorkflowController(CacheableBase):
    """
    __WorkflowController__
    General API for controlling the workflows info
    """

    def __init__(self, wf: str, logger: Optional[Logger] = None, **kwargs) -> None:
        try:
            super(WorkflowController, self).__init__()
            self.logger = logger or getLogger(self.__class__.__name__)

            self.unifiedConfiguration = ConfigurationHandler("config/unifiedConfiguration.json")
            configurationHandler = ConfigurationHandler()
            rucioConfig = {"account": os.getenv("RUCIO_ACCOUNT")}

            self.acdcReader = ACDCReader()
            self.dbsReader = DBSReader()
            self.gwmsReader = GWMSMonReader()
            self.reqmgrReader = ReqMgrReader()
            self.wmstatsReader = WMStatsReader()
            self.wqReader = WorkQueueReader()
            self.oracleReader = OracleClient()
            #self.rucioReader = RucioReader(rucioConfig)

            self.campaignController = None
            self.siteController = None

            self.wf = wf
            self.request = self._getWorkloadHandler(kwargs.get("request"))
            self.spec = None if kwargs.get("noSpec") else self.reqmgrReader.getSpec(wf)
           
        except Exception as error:
            raise Exception(f"Error initializing WorkflowController\n{str(error)}")

    def __str__(self):
        return '%s' % self.wf

    @cached_json('schema', timeout=24*3600)
    def _getWfSchema(self) -> dict:
        """
        The function to get and cache the schema.
        :param: None
        :return: schema dict
        """
        return self.reqmgrReader.getWorkflowSchema(self.wf, makeCopy=True)

    def _getWorkloadHandler(self, wfSchema: Optional[dict] = None) -> BaseWfSchemaHandler:
        """
        The function to set the proper workload handler for a given workflow based on its request type
        :param wfSchema: optional workflow schema
        :return: workload handler
        """
        wfSchema = wfSchema or self._getWfSchema()

        if wfSchema.get("RequestType") == "TaskChain":
            return TaskChainWfSchemaHandler(wfSchema)
        if wfSchema.get("RequestType") == "StepChain":
            return StepChainWfSchemaHandler(wfSchema)
        return BaseWfSchemaHandler(wfSchema)

    def getRequestType(self) -> str:
        """
        Returns request type.
        :return: str, request type.
        """
        return self._getWfSchema().get("RequestType")

    def getUnifiedStatus(self):
        """
        Returns the Unified status of the workflow by querying the Oracle DB.
        :return: str, type.
        """
        return self.oracleReader.session.query(OracleWorkflow).filter(OracleWorkflow.name == self.wf).all()[0].status

    def getRequestStatus(self):
        return self.request.getRequestStatus()

    def _getAllowedSites(self) -> set:
        """
        The function to get the workflow's allowed sites
        :return: site white list
        """
        allowedSites = set()

        lhe, _, _, secondaries = self.request.getIO()
        if lhe:
            return set(sorted(self.siteController.EOSSites))

        if secondaries and self.isHeavyToRead(secondaries):
            for secondary in secondaries:
                allowedSites.update(self.rucioReader.getDatasetLocationsByAccount(secondary, "wmcore_transferor"))
            return set(sorted(allowedSites))

        sites = ["T0Sites", "T1Sites", "goodAAASites" if secondaries else "T2Sites"]
        for site in sites:
            allowedSites.update(getattr(self.siteController, site))

        if self.request.includeHEPCloudInSiteWhiteList:
            allowedSites.update(self.siteController.hepCloudSites)
            self.logger.info("Including HEPCloud in the site white list of %s", self.wf)

        return set(sorted(allowedSites))

    def _restrictAllowedSitesByBlowUpFactor(self, allowedSites: set) -> set:
        """
        The function to restrict a site white list by the workflow's blow up factor
        :param allowedSites: site white list
        :return: new site white list
        """
        blowUp = self.getBlowupFactor()
        maxBlowUp, neededCores = self.unifiedConfiguration.get("blow_up_limits")

        if blowUp > maxBlowUp:
            allowedSitesWithNeededCores = set(
                [site for site in allowedSites if self.siteController.cpuPledges[site] > neededCores]
            )

            if allowedSitesWithNeededCores:
                self.logger.info(
                    "Restricting site white list because of blow-up factors: %s > %s",
                    blowUp,
                    maxBlowUp,
                )

                return allowedSitesWithNeededCores

        return allowedSites

    def _restrictAllowedSitesByCampaign(self, allowedSites: set) -> Tuple[set, set]:
        """
        The function to restrict a site white list by the campaigns' site lists
        :param allowedSites: site white list
        :return: new site white list and site black list
        """
        notAllowedSites = set()

        for campaign in self.request.getCampaigns(details=False):
            allowedCampaignSites = set(self.campaignController.getCampaignValue(campaign, "SiteWhitelist", []))
            if allowedCampaignSites:
                self.logger.info("Restricting site white list by campaign %s", campaign)
                allowedSites = allowedSites & allowedCampaignSites or allowedCampaignSites

            notAllowedCampaignSites = set(self.campaignController.getCampaignValue(campaign, "SiteBlacklist", []))
            if notAllowedCampaignSites:
                self.logger.info("Restricting site white list by black list in campaign %s", campaign)
                notAllowedSites.update(sorted(notAllowedCampaignSites))
                allowedSites -= notAllowedSites

        return allowedSites, notAllowedSites

    def _parseOutputProcessingString(self, processingString: str) -> Tuple[str, str]:
        """
        The function to parse a processing string
        :param processing string: processing string
        :return: parsed acquisition era and processing string
        """
        parsedAcquisitionEra, parsedProcessingString = "*", "*"
        if processingString.count("-") == 2:
            parsedAcquisitionEra, parsedProcessingString, _ = processingString.split("-")
        elif processingString.count("-") == 3:
            parsedAcquisitionEra, _, parsedProcessingString, _ = processingString.split("-")

        if parsedAcquisitionEra in ["None", "FAKE"]:
            acquisitionEra = self.request.getAcquisitionEra()
            self.logger.info("%s has no acquisition era, using %s instead", processingString, acquisitionEra)
            parsedAcquisitionEra = acquisitionEra

        if parsedProcessingString == "None":
            self.logger.info("%s has no processing string, using wildcard char instead", processingString)
            parsedProcessingString = "*"

        return parsedAcquisitionEra, parsedProcessingString

    def _getVersionByWildcardPattern(self, version: Optional[int] = 0) -> Optional[int]:
        """
        The function to get the version by searching the datasets matching a wildcard pattern for the dataset name
        :param version: current version number if known
        :return: version number
        """
        outputDatasets = self.request.get("OutputDatasets", [])

        for dataset in outputDatasets:
            _, name, processingString, tier = dataset.split("/")
            acquisitionEra, processingString = self._parseOutputProcessingString(processingString)

            pattern = self.request.writeDatasetPatternName([name, acquisitionEra, processingString, "v*", tier])
            if not pattern:
                return None

            matches = self.dbsReader.getDatasetNames(pattern, details=False) or []
            self.logger.info("Found %s datasets matching %s", len(matches), pattern)
            for match in matches:
                _, _, matchProcessingString, _ = match.split("/")
                version = max(version, int(matchProcessingString.split("-")[-1].replace("v", "")))

        return version

    def _getVersionByConflictingWorkflows(self, version: Optional[int] = 0) -> int:
        """
        The function to get the version by searching through conflicting workflow versions
        :param version: current version if known
        :return: version number
        """
        outputDatasets = self.request.get("OutputDatasets", [])

        for dataset in outputDatasets:
            _, name, processingString, tier = dataset.split("/")
            acquisitionEra, processingString = self._parseOutputProcessingString(processingString)

            while True:
                expectedName = self.request.writeDatasetPatternName(
                    [name, acquisitionEra, processingString, f"v{version+1}", tier]
                )
                if not expectedName:
                    return version

                conflictingWfs = self.reqmgrReader.getWorkflowsByOutput(expectedName)
                conflictingWfs = [wf for wf in conflictingWfs if wf != self.wf]
                if not conflictingWfs:
                    break

                self.logger.info("There is an output conflict for %s with: %s", self.wf, conflictingWfs)
                version += 1

        return version

    def isHeavyToRead(self, secondaries: Union[list, dict]) -> bool:
        """
        The function to check if it is heavy to read the secondaries
        :param secondaries: secondaries dataset names
        :return: True if minbias appears in secondary, False o/w
        """
        return any("minbias" in secondary.lower() for secondary in secondaries)

    def getRecoveryBlocks(self, suffixTaskFilter: Optional[str] = None) -> Tuple[list, dict, dict, dict]:
        """
        The function to get the blocks needed for the recovery of a workflow
        :param suffixTaskFilter: filter tasks ending with given suffix
        :return: a list of blocks found in DBS, a dict of the blocks locations, a dict of the files locations
        whose blocks were found in DBS, and a dict of the files locations whose blocks were not found in DBS
        """
        try:
            recoveryDocs = self.getRecoveryDocs() or []

            filesAndLocations = DataTools.filterRecoveryFilesAndLocations(recoveryDocs, suffixTaskFilter)
            filesAndLocations, filesAndLocationsWoBlocks = DataTools.filterFilesAndLocationsInDBS(filesAndLocations)

            blocks, blocksAndLocations = self.dbsReader.getRecoveryBlocksAndLocations(filesAndLocations)

            return blocks, blocksAndLocations, filesAndLocations, filesAndLocationsWoBlocks

        except Exception as error:
            self.logger.error("Failed to get recovery blocks")
            self.logger.error(str(error))
            return {}, {}, {}, {}

    def getRecoveryBlocksByTask(self, forSerialization=False) -> Tuple[dict, dict, dict, dict]:
        """
        Same as getRecoveryBlocks, but returns them split by task.
        """
        blocks, blocksAndLocations, filesAndLocations, filesAndLocationsWoBlocks = {}, {}, {}, {}
        for task in self.getErrorTaskNames():
            this_blocks, this_blocksAndLocations, this_filesAndLocations, this_filesAndLocationsWoBlocks = self.getRecoveryBlocks(suffixTaskFilter=task)
            if this_blocks: blocks[task] = this_blocks
            if this_blocksAndLocations: blocksAndLocations[task] = this_blocksAndLocations
            if this_filesAndLocations: filesAndLocations[task] = this_filesAndLocations
            if this_filesAndLocationsWoBlocks: filesAndLocationsWoBlocks[task] = this_filesAndLocationsWoBlocks

        if forSerialization:
            filesAndLocationsWoBlocks_reduced = {}
            nFilesAndLocationsWoBlocks = {}
            for task in filesAndLocationsWoBlocks.keys():
                filesAndLocationsWoBlocks_reduced[task] = {}
                # only keep the first 1 file
                for file in list(filesAndLocationsWoBlocks[task].keys())[:1]:
                    filesAndLocationsWoBlocks_reduced[task][file] = filesAndLocationsWoBlocks[task][file]
                # keep total count of files missing for each task
                nFilesAndLocationsWoBlocks[task] = len(filesAndLocationsWoBlocks[task])
            return blocks, blocksAndLocations, filesAndLocations, filesAndLocationsWoBlocks_reduced, nFilesAndLocationsWoBlocks
        else:
            return blocks, blocksAndLocations, filesAndLocations, filesAndLocationsWoBlocks

    def getRecoveryInfo(self) -> Tuple[dict, dict, dict]:
        """
        The function to get the recovery info
        :return: a dict of task locations, a dict of missing tasks to run, and a dict of missing tasks locations
        """
        try:
            recoveryDocs = self.getRecoveryDocs() or []

            whereToRun = defaultdict(set)
            missingToRun = defaultdict(int)
            whereIsMissingToRun = defaultdict(lambda: defaultdict(int))

            for doc in recoveryDocs:
                task = doc.get("fileset_name", "")
                for filename, data in doc.get("files").items():
                    whereToRun[task].update(
                        self.request.get("SiteWhiteList")
                        if filename.startswith("MCFakeFile")
                        else data.get("locations", [])
                    )

                    missingToRun[task] += data.get("events")
                    for location in data.get("locations", []):
                        whereIsMissingToRun[task][location] += data.get("events")

            whereToRun = mapValues(list, whereToRun)
            whereIsMissingToRun = mapValues(dict, whereIsMissingToRun)

            return whereToRun, dict(missingToRun), whereIsMissingToRun

        except Exception as error:
            self.logger.error("Failed to get recovery info")
            self.logger.error(str(error))
            return {}, {}, {}

    @cached_json('recoveryDocs', timeout=24*3600)
    def getRecoveryDocs(self, cacheLastUpdateLimit: int = 0) -> list:
        """
        The function to get the recovery docs for the workflow
        :param cacheLastUpdateLimit: limit of seconds since a cache file creation for considering it valid
        :return: recovery docs
        """
        try:
            return self.acdcReader.getRecoveryDocs(self.wf)
        except Exception as error:
            self.logger.error("Failed to get recovery docs")
            self.logger.error(str(error))
            return []

    @cached_json('wmerror', timeout=24*3600)
    def getWMErrors(self, cacheLastUpdateLimit: int = 0) -> dict:
        """
        The function to get the WMErrors for the workflow
        :param cacheLastUpdateLimit: limit of seconds since a cache file creation for considering it valid
        :return: WMErrors
        """
        try:
            return self.wmstatsReader.getWMErrors(self.wf)
            
        except Exception as error:
            self.logger.error("Failed to get WMErrors")
            self.logger.error(str(error))
            return {}

    def getWMErrorsSummary(self, getUnreported: bool = True) -> dict:

        try:

            result = self.getWMErrors()
            output = {}

            if not result:
                raise Exception("Failed to get errors from wmstat server for {}: result is {}".format(self.wf, result))

            for stepName, stepData in result.items():
                errors = {}

                for exittype, exittypeData in stepData.items():

                    if exittype.lower() == 'success': continue # don't save successful jobs info

                    for errorCode, errorCodeData in exittypeData.items():
                        sites = {}
                        for site, siteData in errorCodeData.items():
                            if siteData['errorCount']:
                                sites[site] = siteData['errorCount']

                        if sites:
                            errors[errorCode] = sites

                if errors:
                    output[stepName] = errors

            if getUnreported:
                acdcServerResponse = self.getRecoveryDocs() or []

                if 'rows' in acdcServerResponse:
                    for row in acdcServerResponse['rows']:
                        task = row['doc']['fileset_name']

                        newOutput = output.get(task, {})
                        newErrorCode = newOutput.get('-2', {})
                        modified = False
                        for fileReplica in row['doc']['files'].values():
                            for site in fileReplica['locations']:
                                modified = True
                                if site in newErrorCode:
                                    newErrorCode[site] += 1
                                else:
                                    newErrorCode[site] = 1

                        if modified:
                            newOutput['-2'] = newErrorCode
                            output[task] = newOutput

            return output

        except Exception as e:
            self.logger.error('Failed to get errors for %s ' % self.wf)
            self.logger.error(str(e))
            return {}

    def getLogs(self) -> defaultdict(set):
        """
        Get the logs to display on the error report for the workflow.
        :returns: defaultdict of logs organized by task and error code
        """

        errors = self.getWMErrors()
        per_task_explanation = defaultdict(defaultdict)
        for task in errors.keys():
            task_short = task.split("/")[-1]
            per_task_explanation[task_short] = defaultdict(set)
            for exittype in errors[task]:
                for errorcode in errors[task][exittype]:
                    for site in errors[task][exittype][errorcode]:
                        for sample in errors[task][exittype][errorcode][site]['samples']:
                            for step in sample['errors']:
                                for report in sample['errors'][step]:
                                    per_task_explanation[task_short][errorcode].add("%s (Exit code: %s) \n%s"%(report['type'], report['exitCode'], report['details']))


        return per_task_explanation

    @cached_json('wmstats', timeout=24*3600)
    def getWMStats(self, cacheLastUpdateLimit: int = 0) -> dict:
        """
        The function to get the WMStats for the workflow
        :param cacheLastUpdateLimit: limit of seconds since a cache file creation for considering it valid
        :return: WMStats
        """
        try:
            return self.wmstatsReader.getWMStats(self.wf)

        except Exception as error:
            self.logger.error("Failed to get WMStats")
            self.logger.error(str(error))
            return {}

    def getWMStatsSummary(self, bySite: bool = False) -> dict:
        """
        Produces a summary of nSuccess and nFailure per task frm WMStats.
        :return: dict
        """
        try:
            jobStatsPerTaskPerSite = {}
            response = self.getWMStats()
            for agentName, agentData in response['AgentJobInfo'].items():
                for taskName, taskData in agentData['tasks'].items():

                    # ignore logcollect and cleanup tasks
                    if 'status' not in  taskData or 'logcollect' in taskName.lower() or 'cleanup' in taskName.lower():
                        continue
                    else:
                        taskStatus = taskData['status']

                    if taskName not in jobStatsPerTaskPerSite.keys():
                        jobStatsPerTaskPerSite[taskName] = {}

                    # get statuses by site
                    for site, siteData in taskData.get('sites', {}).items():

                        if site not in jobStatsPerTaskPerSite[taskName].keys():
                            jobStatsPerTaskPerSite[taskName][site] = {}

                        for status in ['success','failure','cooloff','submitted']:
                            if not status in siteData: continue

                            if status not in jobStatsPerTaskPerSite[taskName][site].keys():
                                jobStatsPerTaskPerSite[taskName][site][status] = 0

                            data = siteData[status]
                            if type(data) is dict:
                                jobStatsPerTaskPerSite[taskName][site][status] += sum( data.values() )
                            else:
                                jobStatsPerTaskPerSite[taskName][site][status] += data
            
                    # skipped need to handled differently
                    for site, siteData in taskData.get('skipped', {}).items():

                        if site not in jobStatsPerTaskPerSite[taskName].keys():
                            jobStatsPerTaskPerSite[taskName][site] = {}
                        
                        if 'nSkipped' not in jobStatsPerTaskPerSite[taskName][site].keys():
                            jobStatsPerTaskPerSite[taskName][site]['nSkipped'] = 0

                        nSkipped = siteData.get('skippedFiles', 0)
                        jobStatsPerTaskPerSite[taskName][site]['nSkipped'] += nSkipped
                        

            # return the full dict if bySite is True
            if bySite:
                return jobStatsPerTaskPerSite
            # 'integrate' over the sites to just return the total by status for each task
            else:
                jobStatsPerTask = {}

                for task, sites in jobStatsPerTaskPerSite.items():
                    task_dict = {}
                    for site, status_counts in sites.items():
                        for status, count in status_counts.items():
                            if status in task_dict:
                                task_dict[status] += count
                            else:
                                task_dict[status] = count
                    jobStatsPerTask[task] = task_dict

                return jobStatsPerTask

        except Exception as e:
            self.logger.error("Failed to return summary of WMStats.")
            self.logger.error(str(e))
            return {}

    def getFailureRate(self) -> dict:
        """
        :param None
        :returns: a dictionary containing failure rates for each task/step in the following format::
                  {task: failure_rate}
        :rtype: dict 
        """

        try:
            failureRatePerTask = {}
            jobStats = self.getWMStatsSummary()

            for taskName, stats in jobStats.items():
                if 'nFailure' not in stats.keys() or 'nSuccess' not in stats.keys(): continue
                if stats['nFailure'] + stats['nSuccess'] == 0:
                    failureRatePerTask[taskName] = -1
                else:
                    failureRatePerTask[taskName] = stats['nFailure'] / (stats['nFailure'] + stats['nSuccess'])
            return failureRatePerTask
        except Exception as e:
            self.logger.error('Failed to get failure rate for %s ' % self.wf)
            self.logger.error(str(e))
            return {}

    def getFamily(self, onlyResubmissions: bool = False, includeItself: bool = False) -> list:
        """
        The function to get the request family
        :param onlyResubmissions: if to only include resubmissions
        :param includeItself: if to include itself
        :return: request family
        """
        try:
            possibleFamily = self.reqmgrReader.getWorkflowsByPrepId(self.request.get("PrepID"), details=True)

            family = []
            for member in possibleFamily:
                if (
                    member.get("RequestDate") < self.request.get("RequestDate")
                    or str(member.get("RequestStatus")) == "None"
                ):
                    continue

                itself = member.get("RequestName") == self.request.get("RequestName")
                resubmitted = member.get("RequestType") == "Resubmission"

                if (
                    (includeItself and itself)
                    or (onlyResubmissions and resubmitted and not itself)
                    or (not onlyResubmissions and not itself)
                ):
                    family.append(member)

            return family

        except Exception as error:
            self.logger.error("Failed to get family")
            self.logger.error(str(error))

    def getAllTasks(self, **selectParam) -> list:
        """
        The function to get all tasks in the workflow
        :param selectParam: optional task selection params
        :return: list of tasks
        """
        try:
            spec = self.spec or self.reqmgrReader.getSpec(self.wf)

            allTasks = []
            for task in spec.tasks.tasklist:
                taskSpec = getattr(spec.tasks, task)
                allTasks.extend(DataTools.flattenTaskTree(taskSpec, **selectParam))

            return allTasks

        except Exception as error:
            self.logger.error("Failed to get tasks")
            self.logger.error(str(error))

    def filterTaskNames(self, tasks):
        """
        :param: list of tasks (strings)
        :returns: list of task names filtered.
        :rtype: list of str
        """

        filteredTasks = []
        for task in tasks:
            if any([v in task.lower() for v in ['logcollect','cleanup']]): continue
            filteredTasks.append(task)
        return filteredTasks

    def getErrorTaskNames(self) -> list:
        """
        :param: None
        :returns: list of Tasks of the given workflow.
                  N.B.: these are not all the steps in a StepChain, these are all the tasks
                  for which error codes exist, i.e. in the WM agent json, used by getErrors,
                  they are the AgentJobInfo tasks.
        :rtype: list of str
        """
        return self.filterTaskNames(list(self.getWMErrorsSummary().keys()))

    def getWorkTasks(self) -> list:
        """
        The function to get the work tasks in the workflow
        :return: list of work tasks
        """
        return self.getAllTasks(taskType=["Production", "Processing", "Skim", "Merge"])

    def getFirstTask(self) -> str:
        """
        The function to get the workflow's first task
        :return: first task
        """
        return (self.spec or self.reqmgrReader.getSpec(self.wf)).tasks.tasklist[0]

    def getOutputDatasetsPerTask(self) -> dict:
        """
        The function to get the output datasets by task
        :return: a dict of dataset names by task names
        """
        return self.request.getOutputDatasetsPerTask(self.getWorkTasks())

    def getCampaignByTask(self, task: str) -> str:
        """
        The function to get the campaign for a given task
        :param task: task name
        :return: campaign
        """
        return self.request.getParamByTask("Campaign", task)

    def getTasksCampaigns(self) -> dict:
        """
        Returns a dictionary with campaign for each task.
        """
        output = {}
        tasks = self.getErrorTaskNames()
        for task in tasks:
            output[task] = self.getCampaignByTask(task)
        return output

    def getMemoryByTask(self, task: str) -> int:
        """
        The function to get the memory used by task
        :param task: task name
        :return: memory
        """
        return int(self.request.getParamByTask("Memory", task) or 0)

    def getCoreByTask(self, task: str) -> int:
        """
        The function to get the cores used by task
        :param task: task name
        :return: number of cores
        """
        return int(self.request.getParamByTask("Multicore", task) or 1)

    def getFilterEfficiencyByTask(self, task: str) -> float:
        """
        The function to get the filter efficiency by task
        :param task: task name
        :return: filter efficiency
        """
        return float(self.request.getParamByTask("FilterEfficiency", task) or 1)

    def getBlockWhiteList(self) -> list:
        """
        The function to get the workflow's block white list
        :return: block white list
        """
        return self.request.getParamList("BlockWhitelist")

    def getRunWhiteList(self) -> list:
        """
        The function to get the workflow's run white list
        :return: run white list
        """
        return self.request.getParamList("RunWhitelist")

    def getSiteWhiteList(self, pickOne: bool = False) -> Tuple[list, list]:
        """
        The function to get the site white list
        :param pickOne: pick one site from CE list, o/w keep all sites
        :return: site white list, site black list
        """
        try:
            if self.siteController is None:
                self.siteController = SiteController()
            if self.campaignController is None:
                self.campaignController = CampaignController()
            
            allowedSites = self._getAllowedSites()
            if pickOne:
                allowedSites = set(sorted(self.siteController.pickCE(allowedSites)))

            self.logger.info("Initially allow %s", allowedSites)

            allowedSites = self._restrictAllowedSitesByBlowUpFactor(allowedSites)
            allowedSites, notAllowedSites = self._restrictAllowedSitesByCampaign(allowedSites)

            self.logger.info("Allowed sites: %s", allowedSites)
            self.logger.info("Not allowed sites: %s", notAllowedSites)
            return allowedSites, notAllowedSites

        except Exception as error:
            self.logger.error("Failed to get site white list")
            self.logger.error(str(error))

    def getPrepId(self) -> list:
        """
        The function to get the workflow prep ids
        :return: list of prep ids
        """
        return self.request.get("PrepID")

    def getPrepIds(self) -> list:
        """
        The function to get the workflow prep ids
        :return: list of prep ids
        """
        return self.request.getParamList("PrepID")

    def getScramArches(self) -> list:
        """
        The function to get the scram arches
        :return: scram arches
        """
        return self.request.getParamList("ScramArch")

    def getPercentCompletions(self):
        return self.request.getPercentCompletions()

    def getParentTaskName(self):
        """
        :param None
        :returns: the parent task. Parent task is the one for which the ACDC/recovery is created
        :rtype: str
        """
        return self.request.getParentTaskName()

    def getParentWorkflowName(self):
        """
        :param None
        :returns: the parent workflow. Parent workflow is the one for which the ACDC/recovery is created
        :rtype: ste
        """
        return self.request.getParentWorkflowName()

    def getLabels(self) -> list:
        """
        Returns JIRA labels for the workflow.
        :return: list of labels
        """
        from WorkflowMgmt.PrepID import PrepID

        labels = []
        for prepIDName in self.getPrepIds():
            prepID = PrepID(prepIDName)
            labels.extend(prepID.getLabels())
        return labels

    def getComputingTime(self, unit: str = "h") -> float:
        """
        The function to get the computing time
        :param unit: time unit — s, m, h or d. Non valid units will return computing time in seconds
        :return: computing time
        """
        try:
            div = 60.0 if unit == "m" else 3600.0 if unit == "h" else 86400.0 if unit == "d" else 1.0
            return self.request.getComputingTime() / div

        except Exception as error:
            self.logger.error("Failed to get computing time")
            self.logger.error(str(error))

    def getBlocks(self) -> List[str]:
        """
        The function to get all blocks
        :return: list of block names
        """
        try:
            _, primaries, _, _ = self.request.getIO()
            blocks = set(self.getBlockWhiteList())

            runs = self.getRunWhiteList()
            if runs:
                runBlocks = [self.dbsReader.getDatasetBlockNamesByRuns(primary, runs) for primary in primaries]
                blocks.update(*runBlocks)

            lumis = self.request.getLumiWhiteList()
            if lumis:
                lumisBlocks = [self.dbsReader.getDatasetBlockNamesByLumis(primary, lumis) for primary in primaries]
                blocks.update(*lumisBlocks)

            return list(blocks)

        except Exception as error:
            self.logger.error("Failed to get blocks")
            self.logger.error(str(error))

    def getAge(self) -> int:
        return self.request.getAge()

    def getOriginalIO(self) -> Tuple[bool, set, set, set]:
        """
        Get the IO for the original workflow.
        :return: lhe, primaries, parents, secondaries
        """
        ancestor = self.getAncestor()
        lhe, primaries, parents, secondaries = ancestor.request.getIO()
        return lhe, primaries, parents, secondaries

    def getAncestor(self):
        """
        Returns the original workflow.
        :return: WorkflowController object of original workflow.
        """
        ancestor = self
        while ancestor.getRequestType() == 'Resubmission':
            ancestor = WorkflowController(ancestor.request.get('OriginalRequestName'))
        return ancestor

    def getAgents(self) -> dict:
        """
        The function to get the workflow's agents
        :return: agents
        """
        try:
            agents = defaultdict(lambda: defaultdict(int))

            workQueue = self.workqueue or self.wqReader.getWorkQueue(self.wf)
            workers = [worker.get(worker.get("type")) for worker in workQueue]

            for status in set([worker.get("Status") for worker in workers]):
                statusWorkers = [worker for worker in workers.get("Status") == status]
                for statusWorker in statusWorkers:
                    agents[status][statusWorker.get("ChildQueueUrl")] += 1

            return mapValues(dict, agents)

        except Exception as error:
            self.logger.error("Failed to get the agents")
            self.logger.error(str(error))

    def getSplittings(self) -> List[dict]:
        """
        The function to get the splittings for the workflow tasks
        :return: a list of dicts
        """
        try:
            keysToKeep = [
                "events_per_lumi",
                "events_per_job",
                "lumis_per_job",
                "halt_job_on_file_boundaries",
                "max_events_per_lumi",
                "halt_job_on_file_boundaries_event_aware",
            ]
            algorithmsToKeep = {
                "EventAwareLumiBased": {"halt_job_on_file_boundaries_event_aware": "True"},
                "LumiBased": {"halt_job_on_file_boundaries": "True"},
            }
            algorithmsToTranslate = {"EventAwareLumiBased": {"events_per_job": "avg_events_per_job"}}

            splittings = []
            for task in self.getWorkTasks():
                taskSplitting = task.input.splitting
                splitting = {"splittingAlgo": taskSplitting.algorithm, "splittingTask": task.pathName}

                if taskSplitting.algorithm in algorithmsToKeep:
                    splitting.update(algorithmsToKeep[taskSplitting.algorithm])

                for key in keysToKeep:
                    if hasattr(taskSplitting, key):
                        splittingsKey = key
                        if taskSplitting.algorithm in algorithmsToTranslate:
                            splittingsKey = algorithmsToTranslate[taskSplitting.algorithm].get(key) or key
                        splitting.update({splittingsKey: getattr(taskSplitting, key)})

                splittings.append(splitting)

            return splittings

        except Exception as error:
            self.logger.error("Failed to get splittings")
            self.logger.error(str(error))

    def getSplittingsSchema(self, strip: bool = False, allTasks: bool = False) -> List[dict]:
        """
        The function to get splittings schema for the workflow
        :param strip: if True it will drop some split params, o/w it will keep all params
        :param allTasks: if True it will keep all tasks types, o/w it will keep only production, processing and skim tasks
        :return: a list of dicts
        """
        try:
            splittings = self.reqmgrReader.getSplittingsSchema(self.wf)

            if not allTasks:
                splittings = DataTools.filterSplittingsTaskTypes(splittings)
            if strip:
                splittings = DataTools.filterSplittingsParam(splittings)

            return splittings

        except Exception as error:
            self.logger.error("Failed to get splittings schema")
            self.logger.error(str(error))

    def getConfigCacheID(self) -> dict:
        """
        The function to get the cache id configuration
        :return: cache id configuration
        """
        try:
            config = {}
            for task in self.getWorkTasks():
                name = task.pathName.split("/")[-1]
                configId = task.steps.cmsRun1.application.configuration.configId
                config[name] = configId

            return config

        except Exception as error:
            self.logger.error("Failed to get cache id configuration")
            self.logger.error(str(error))

    def getBlowupFactor(self) -> float:
        """
        The function to get the workflow's blow up factor
        :return: blow up
        """
        return self.request.getBlowupFactor(self.getSplittings())

    def getCompletionFraction(self, withEvents: bool = True) -> dict:
        """
        The function to get the completion fraction of the output datasets
        :param withEvents: compute completion fraction using events if True, use only lumis o/w
        :return: a dict of dataset names by completion fraction
        """
        try:
            percentCompletion = defaultdict(float)

            expectedLumis = float(self.request.get("TotalInputLumis", 0))
            expectedEventsPerTask = self.request.getExpectedEventsPerTask()

            tasksPerOutput = self.request.getTasksPerOutputDatasets(self.getWorkTasks()) or {}

            for dataset in self.request.get("OutputDatasets", []):
                events, lumis = self.dbsReader.getDatasetEventsAndLumis(dataset)
                if expectedLumis:
                    percentCompletion[dataset] = lumis / expectedLumis
                    self.logger.info("%s with lumi completion of %s of %s", dataset, lumis, expectedLumis)

                datasetExpectedEvents = expectedEventsPerTask.get(tasksPerOutput.get(dataset, "NoTaskFound"))
                if datasetExpectedEvents and withEvents:
                    eventFraction = events / datasetExpectedEvents
                    if eventFraction > percentCompletion[dataset]:
                        percentCompletion[dataset] = eventFraction
                        self.logger.info(
                            "Overriding: %s with event completion of %s of %s", dataset, events, datasetExpectedEvents
                        )

            return dict(percentCompletion)

        except Exception as error:
            self.logger.error("Failed to get completion fraction")
            self.logger.error(str(error))

    def getNCopies(
        self, CPUh: Optional[float] = None, m: int = 2, M: int = 3, w: int = 50000, C0: int = 100000
    ) -> int:
        """
        The function to get the number of needed copies based on the computing time
        :param CPUh: computing hours
        :return: number of required copies
        """
        try:
            CPUh = CPUh or self.getComputingTime()

            sigmoid = lambda x: 1 / (1 + math.exp(-x))
            f = sigmoid(-C0 / w)
            D = (M - m) / (1 - f)
            O = (f * M - m) / (f - 1)

            return int(O + D * sigmoid((CPUh - C0) / w))

        except Exception as error:
            self.logger.error("Failed to compute needed copies")
            self.logger.error(str(error))

    def getNextVersion(self) -> int:
        """
        The function to get the next processing version
        :return: next version
        """
        try:
            version = max(0, int(self.request.get("ProcessingVersion", 0)) - 1)
            version = self._getVersionByWildcardPattern(version)
            version = self._getVersionByConflictingWorkflows(version)

            return version + 1

        except Exception as error:
            self.logger.error("Failed to get next version")
            self.logger.error(str(error))

    def isRecovery(self) -> bool:
        return self.request.isRecovery()

    def getGlideWMSMonSummary(self):
        """
        The function to get the glide mon summary
        :return: glide mon summary
        """
        return self.gwmsReader.getRequestSummary(self.wf)

    def getSummary(self) -> dict:
        """
        The function to get the workflow request summary
        :return: summary
        """
        summary = self.reqmgrReader.getWorkflowSummary(self.wf)
        return summary

    def checkSplittings(self) -> Tuple[bool, list]:
        """
        The function to check the splittings
        :return: if to hold and a list of modified splittings
        """
        return self.request.checkSplittings(self.getSplittingsSchema(strip=True))

    def go(self, silent: bool = False) -> bool:
        """
        The function to check if a workflow is allowed to go
        :param silent: if True no logs are sent
        :return: True if allowed to go, False o/w
        """
        try:
            campaignsAndLabels = self.request.getCampaignsAndLabels()
            for campaign, label in campaignsAndLabels:
                if "pilot" in label.lower():
                    if not silent:
                        self.logger.info(
                            "pilot keyword in processing string %s in campaign %s, assigning the workflow",
                            label,
                            campaign,
                        )
                    return True

            if "pilot" in self.request.get("SubRequestType", ""):
                if not silent:
                    self.logger.info("pilot keyword in SubRequestType, assigning the workflow")
                return True

            if self.campaignController is None:
                self.campaignController = CampaignController()
            for campaign, label in campaignsAndLabels:
                if not self.campaignController.go(campaign, label):
                    if not silent:
                        self.logger.info("No go due to %s, %s", campaign, label)
                    return False

            return True

        except Exception as error:
            self.logger.error("Failed to check if allowed to go or not")
            self.logger.error(str(error))
