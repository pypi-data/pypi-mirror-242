from MongoControllers.AssistanceController import AssistanceController
from Databases.Oracle.OracleClient import OracleClient
from Databases.Oracle.OracleDB import Workflow as OracleWorkflow
from Utilities.Logging import getLogger
from Utilities.ConfigurationHandler import ConfigurationHandler
from Utilities.Decorators import runWithMultiThreading
from Services.ServicesChecker import ServicesChecker
from MongoControllers.ModuleLockController import ModuleLockController
from WorkflowMgmt.WorkflowController import WorkflowController
from WorkflowMgmt.PrepID import PrepID

import optparse
from typing import List, Optional, Tuple
from logging import Logger
import traceback
import sys
import time


class Serializor(OracleClient):

    def __init__(self, logger: Optional[Logger] = None, **kwargs) -> None:
        try:
            super().__init__(self)
            self.logger = logger or getLogger(self.__class__.__name__)

            self.assistanceController = AssistanceController()

            self.options = kwargs.get("options", {})
            if self.options is {}:
                self.options = self.parseOptions()

            unifiedConfiguration = ConfigurationHandler(
                "config/unifiedConfiguration.json"
            )
            self.users = {
                "pnr": unifiedConfiguration.get("pnr_users"),
                "rereco": unifiedConfiguration.get("rereco_users"),
                "relval": unifiedConfiguration.get("relval_users"),
            }

        except Exception as error:
            raise Exception(f"Error initializing Serializor\n{str(error)}")

    @staticmethod
    def parseOptions() -> Optional[dict]:
        """
        The function to parse the Injector's options and specific workflow
        :return: options and the specific workflow, if any
        """
        parser = optparse.OptionParser()

        parser.add_option('--status', '-s', help="Statuses you want to serialize.",
                          default=None)
        parser.add_option('--workflow', '-w', help="The workflow you want to serialize",
                          default=None)
        parser.add_option('--max', '-m', help="Maximum number of workflows you want to serialize",
                          default=-1)
        parser.add_option('--clean', '-c', help="Clean each workflow in mongoDB before you serialize", action='store_true',
                          default=False)
        parser.add_option('--cached', help="Use cached info for Workflows", action='store_true',
                          default=False)
        parser.add_option('--purgeOlderThan', '-p', default=-1, type=float, help="Clears the mongoDB collection before running from workflows older than N days (default: -1 days).")

        options, args = parser.parse_args()

        if sum([options.status is None, options.workflow is None]) != 1:
            raise Exception("One of --status or --workflow must be specified.")

        return vars(options)

    def ignoreMinus2(self, error_dict) -> None:
        """
        Remove exitCode -2, if there are other exitCodes in the wf
        """
        tasks = list(error_dict.keys())
        for task in tasks:
            exitCodes = list(set(list(error_dict[task].keys())))
            if "-2" in exitCodes and len(exitCodes) > 1:
                error_dict[task].pop('-2')

    def setWorkflowAttribute(self, workflowName: str, attribute: str, data) -> None:
        """
        Set attribute for workflow using the functions from AssistanceController.
        """
        setWorkflowAttribute = getattr(self.assistanceController, f"setWorkflow{attribute}")
        setWorkflowAttribute(workflowName, data)

    def setTasksAttribute(self, workflowName: str, attribute: str, data) -> None:
        """
        Set attribute for many tasks at once using the functions from AssistanceController.
        """
        for task, content in data.items():
            setWorkflowAttribute = getattr(self.assistanceController, f"setWorkflow{attribute}")
            setWorkflowAttribute(workflowName, task, content)

    def collectAndSetWorkflowData(self, workflowName: str) -> dict:
        """
        Use the the WorkflowController, PrepID to collect all relevant
        information about the workflow you want to store in the database.
        Store it using the setWorkflowXYZ functions of AssistanceController
        through setTasksAttribute.

        Input: workflow name
        Output: dict
        """
        data = {}
        wf = WorkflowController(workflowName)
        if self.options.get("cached") is False:
            wf.reset()

        # workflow level data
        _,primary,_,secondary = wf.getOriginalIO()
        self.setWorkflowAttribute(workflowName, 'RequestType', wf.getRequestType())
        self.setWorkflowAttribute(workflowName, 'PrepID', wf.getPrepId())
        self.setWorkflowAttribute(workflowName, 'PrepIDs', wf.getPrepIds())
        self.setWorkflowAttribute(workflowName, 'PercentCompletions', wf.request.getPercentCompletions())
        self.setWorkflowAttribute(workflowName, 'ReqMgrStatus', wf.request.getRequestStatus())
        self.setWorkflowAttribute(workflowName, 'UnifiedStatus', wf.getUnifiedStatus())
        self.setWorkflowAttribute(workflowName, 'Primary', primary)
        self.setWorkflowAttribute(workflowName, 'Secondary', secondary)
        self.setWorkflowAttribute(workflowName, 'OutputDatasets', wf.request.getOutputDatasets())

        # prep ID level data
        self.setWorkflowAttribute(workflowName, 'Labels', wf.getLabels())

        # task level data
        wfErrors = wf.getWMErrorsSummary()
        self.ignoreMinus2(wfErrors)
        blocks, blocksAndLocations, filesAndLocations, filesAndLocationsWoBlocks_reduced, nFilesAndLocationsWoBlocks = wf.getRecoveryBlocksByTask(forSerialization=True)
        _, _,missing_to_run_at = wf.getRecoveryInfo()       
        self.setTasksAttribute(workflowName, "Errors", wfErrors)
        self.setTasksAttribute(workflowName, "FailureRate", wf.getFailureRate())
        self.setTasksAttribute(workflowName, "JobStats", wf.getWMStatsSummary(bySite=True))
        self.setTasksAttribute(workflowName, "Campaign", wf.getTasksCampaigns())
        self.setTasksAttribute(workflowName, "Blocks", blocksAndLocations)
        self.setTasksAttribute(workflowName, "UFiles", filesAndLocationsWoBlocks_reduced)
        self.setTasksAttribute(workflowName, "NUFiles", nFilesAndLocationsWoBlocks)
        self.setTasksAttribute(workflowName, "Files", filesAndLocations)
        self.setTasksAttribute(workflowName, "Missing", missing_to_run_at)
        self.setTasksAttribute(workflowName, "Logs", wf.getLogs())
        self.setTasksAttribute(workflowName, "FilterEfficiency", {task: wf.getFilterEfficiencyByTask(task) for task in wfErrors.keys()})

    def getWorkflowNamesToProcess(self) -> list:
        """
        Get all the workflow names we want to process with this run.
        """
        if self.options.get('status'):
            # collect all workflows we want to update from Oracle
            workflows = self.session.query(OracleWorkflow).filter(
                OracleWorkflow.status.contains(self.options.get('status'))
            ).all()
            workflowNames = [wf.name for wf in workflows]
        else:
            workflowNames = [self.options.get("workflow")]

        if options.get("max", -1) > 0:
            workflowNames = workflowNames[:options.get("max")]

        self.logger.info(f"Workflows to process: \n {workflowNames}")
        return workflowNames

    @runWithMultiThreading(mtParam='workflowNames', timeout=300, wait=10)
    def serializeWorkflows(self, workflowNames) -> bool:
        try:
            # wipe the entry for this workflow if requested
            if self.options.get("clean"):
                self.assistanceController.cleanWorkflow(workflowNames)

            # get relevant data about the worklfow
            thisWfData = self.collectAndSetWorkflowData(workflowNames)

            self.logger.info(f"Workflow {workflowNames} has been serialized.")

            return True

        except Exception as error:
            self.logger.error(
                "Failed to run serialization for {}.".format(workflowNames))
            self.logger.error(str(error))
            self.logger.error(traceback.format_exc())
            return False

    def go(self) -> bool:
        """
        The function to check if the injector can go
        :return: True if it can go, False o/w
        """
        try:
            moduleLockController = ModuleLockController()
            servicesChecker = ServicesChecker(
                softServices=["mcm", "wtc", "jira", "eos"])

            return (self.options.get("workflow") or not moduleLockController.isLocked()) and servicesChecker.check()

        except Exception as error:
            self.logger.error("Failed to check if Serializor can go")
            self.logger.error(str(error))
            return False

    def run(self) -> None:
        """
        The function to run the serialization.
        """

        try:

            # purge older workflows, if requested
            if self.options.get("purgeOlderThan") > 0:
                self.assistanceController.purge(self.options.get("purgeOlderThan"))

            # serialize!
            start = time.time()
            workflowNames = self.getWorkflowNamesToProcess()     
            results = self.serializeWorkflows(workflowNames=workflowNames)
            end = time.time()

            self.logger.info("Of {} workflows, {} succeeded, and {} failed.".format(len(results), sum(results), len(results) - sum(results)))
            self.logger.info("Time spent: {} seconds.".format(round(end - start)))

        except Exception as error:
            self.logger.error("Failed to run serialization.")
            self.logger.error(str(error))
            self.logger.error(traceback.format_exc())


if __name__ == "__main__":
    options = Serializor.parseOptions()
    serializor = Serializor(options=options)

    if serializor.go():
        serializor.run()
    else:
        logger = getLogger("Serializor")
        logger.critical("Serializor isn't allowed run")
