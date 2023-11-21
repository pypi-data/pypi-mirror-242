"""
File       : PrepID.py
Author     : Hasan Ozturk <haozturk AT cern dot com>
Description: PrepID class which provides all the information needed in prepID level.
"""

import os
import operator
from collections import defaultdict
from logging import Logger
from types import prepare_class
from typing import Optional, Tuple, List, Union

from WorkflowMgmt.CacheableBase import CacheableBase,cached_json
from WorkflowMgmt.WorkflowController import WorkflowController

from Services.ReqMgr.ReqMgrReader import ReqMgrReader
from Services.Jira.JiraReader import JiraReader

from Utilities.ConfigurationHandler import ConfigurationHandler
from Utilities.IteratorTools import mapValues
from Utilities import DataTools
from Utilities.Logging import getLogger


class PrepID(CacheableBase):

    def __init__(self, prepID: str, logger: Optional[Logger] = None, **kwargs) -> None:
        try:
            super(PrepID, self).__init__()
            self.logger = logger or getLogger(self.__class__.__name__)

            self.unifiedConfiguration = ConfigurationHandler("config/unifiedConfiguration.json")
            configurationHandler = ConfigurationHandler()

            self.reqmgrReader = ReqMgrReader()
            self.jiraReader = JiraReader()

            self.prepID = prepID

        except Exception as error:
            raise Exception(f"Error initializing PrepID\n{str(error)}")

    def reset(self):
        """
        The WorkflowController objects are stored in a cache. At times,
        in order to get the latest info, we want to reset this cache.
        This function resets the cache for all workflows in this PrepID.
        """
        workflows = self.getWorkflows()
        for wf in workflows: wf.reset()

    def getWorkflowNames(self):
        """
        :param None
        :returns: list of workflow names under the given prepID
        :rtype: list of str
        """
        return self.reqmgrReader.getWorkflowsByPrepId(pid=self.prepID, details=False)

    def getWorkflows(self):
        """
        :param None
        :returns: list of Workflow objects under the given prepID
        :rtype: list of WorkflowController objects
        """
        workflowNames = self.getWorkflowNames()
        workflows = [WorkflowController(workflow) for workflow in workflowNames] # list of WorkflowController objects
        return workflows

    def getOriginalWorkflow(self):
        """
        :param None
        :returns: the original workflow of the given prepID
                : The original workflow is the oldest active workflow
        :rtype: WorkflowController object
        """
        workflows = self.getWorkflows()
        activeWorkflows = self.removeRejectedWorkflows(workflows)
        return max(activeWorkflows, key=lambda x: x.getAge())

    def getRecentWorkflows(self):
        """
        :param None
        :returns: the most recent workflow(s) under the given prepID. These workflows are the ones for which we need to
                  take action, i.e. they are the ones for which no ACDC/recovery is created.
                  For instance, if there is only one (original) workflow, then that should be returned.
                  If there is one original, 3 ACDC0 and 2 ACDC1 and 2 ACDC2 workflows, then the 2 ACDC2s should be returned.
        :rtype: list of WorkflowController objects
        """
        originalWorkflow = self.getOriginalWorkflow()
        if originalWorkflow.getRequestType() == 'ReReco':
            return self.getRecentWorkflowsReReco()
        else:
            return self.getRecentWorkflowsMC()

    def getRecentTasks(self):
        """
        :param None
        :returns: the most recent task(s) under the given prepID. These tasks are the ones for which we need to
                  take action, i.e. they are the ones for which no ACDC/recovery is created.
                  For instance, if there is only one (original) workflow, then that should be returned.
                  If there is one original, 3 ACDC0 and 2 ACDC1 and 2 ACDC2 workflows, then the 2 ACDC2s should be returned.
        :rtype: list of tasks
        """
        originalWorkflow = self.getOriginalWorkflow()
        if originalWorkflow.getRequestType() == 'ReReco':
            return self.getRecentTasksReReco()
        else:
            return self.getRecentTasksMC()

    def getRecentWorkflowsMC(self):
        """
        :param None
        :returns: the most recent workflow(s) under the given prepID. It covers the MC workflows
        :rtype: list of Workflow objects
        """
        workflows = self.getWorkflows()
        activeWorkflows = self.removeRejectedWorkflows(workflows)

        # Populate the parentWorkflows, i.e. the ones for which an ACDC/recovery is created
        parentWorkflowNames = set()
        for workflow in activeWorkflows:
            parentWorkflowName = workflow.getParentWorkflowName()
            if parentWorkflowName:
                parentWorkflowNames.add(parentWorkflowName)

        recentWorkflows = []
        for workflow in activeWorkflows:
            if workflow.wf not in parentWorkflowNames:
                recentWorkflows.append(workflow)

        return recentWorkflows

    def getRecentTasksMC(self):
        """
        :param None
        :returns: the most recent task(s) under the given prepID. It covers the MC workflows
        :rtype: list of tasks
        """
        workflows = self.getWorkflows()
        activeWorkflows = self.removeRejectedWorkflows(workflows)

        # get all tasks for active workflows
        activeTasks = []
        for wf in activeWorkflows:
            activeTasks += wf.getErrorTaskNames()

        # Populate the parentTasks, i.e. the ones for which an ACDC/recovery is created
        parentTaskNames = set()
        for workflow in activeWorkflows:
            parentTaskName = workflow.getParentTaskName()
            if parentTaskName:
                parentTaskNames.add(parentTaskName)

        # recent tasks are defined to be the ones that have not been ACDC'd already
        recentTasks = []
        for task in activeTasks:
            if task not in parentTaskNames:
                recentTasks.append(task)

        return recentTasks

    def getRecentWorkflowsReReco(self):
        """
        :param None
        :returns: the most recent workflow(s) under the given prepID. This function covers the special cases for ReReco
                  workflows such as recovery workflows which are different from regular ACDCs.
        :rtype: list of Workflow objects
        """
        recentWorkflows = []
        youngestWorkflow = self.getYoungestWorkflow()
        if youngestWorkflow.isRecovery():
            # If the youngest workflow is a recovery, then return the latest recovery workflows
            workflows = self.getWorkflows()
            activeWorkflows = self.removeRejectedWorkflows(workflows)

            for workflow in activeWorkflows:
                if workflow.isRecovery():
                    # A lazy workaround: Latest recovery workflows are submitted more or less  at the same time.
                    # Here, we return all recovery workflows in a 1 hour time window based on the youngest one
                    if youngestWorkflow.getAge() - workflow.getAge() < 3600:
                        recentWorkflows.append(workflow)
            return recentWorkflows
        else:
            # if youngest workflow is not a recovery, then regular MC function works
            return self.getRecentWorkflowsMC()

    def getRecentTasksReReco(self):
        """
        :param None
        :returns: the most recent workflow(s) under the given prepID. This function covers the special cases for ReReco
                  workflows such as recovery workflows which are different from regular ACDCs.
        :rtype: list of Workflow objects
        """
        youngestWorkflow = self.getYoungestWorkflow()
        if youngestWorkflow.isRecovery():
            # If the youngest workflow is a recovery, then return the latest recovery workflows
            workflows = self.getWorkflows()
            activeWorkflows = self.removeRejectedWorkflows(workflows)

            recentWorkflows = []
            for workflow in activeWorkflows:
                if workflow.isRecovery():
                    # A lazy workaround: Latest recovery workflows are submitted more or less  at the same time.
                    # Here, we return all recovery workflows in a 1 hour time window based on the youngest one
                    if youngestWorkflow.getAge() - workflow.getAge() < 3600:
                        recentWorkflows.append(workflow)

            # get all tasks for active fworkflows
            activeTasks = []
            for wf in recentWorkflows:
                activeTasks += wf.getTaskNames()

            return activeTasks
        else:
            # if youngest workflow is not a recovery, then regular MC function works
            return self.getRecentTasksMC()

    def getLabels(self):
        """
        :param: None
        :returns: list of labels of the given prepID which are in sync with JIRA
        :rtype: list of strings
        """
        tickets = self.jiraReader.find({'prepID': self.prepID})
        if len(tickets) == 0:
            ## TODO: Create a ticket for every workflow in assistance (Checkor module)
            self.logger.warning("There is no JIRA ticket for %s" % self.prepID)
            labels = []
        else:
            ## pick up the last one
            self.logger.warning("There is at least one JIRA ticket for %s, taking the last one" % self.prepID)
            ticket = sorted(tickets, key=lambda t: self.jiraReader.getTicketCreationTime(t))[-1]
            labels = ticket.fields.labels

        return labels

    def getCampaigns(self):
        """
        :param None
        :returns: campaigns of the given prepID
        :rtype: list of strings
        """
        pass

    def getPrimaryDataset(self):
        """
        :param None
        :returns: PD of the given prepID
        :rtype: string
        """
        pass

    def getSecondaryDatasets(self):
        """
        :param None
        :returns: secondary datasets of the given prepID
        :rtype: list of strings
        """
        pass

    def getPrimaryDatasetLocation(self):
        """
        :param None
        :returns: Location(s) of the PD
        :rtype: To be discussed (PD could be distributed over the grid)
        """
        pass

    def getSecondaryDatasetsLocation(self):
        """
        :param None
        :returns: Location(s) of the SD
        :rtype: To be discussed (SD could be distributed over the grid)
        """
        pass

    def getErrors(self):
        """
        :param None
        :returns: a dictionary containing error codes and number of failed jobs for each task/step in the following format::
                  {task: {errorcode: {site: failed_job_count}}}
        :rtype: dict
        """
        pass

    def getFailureRate(self):
        """
        :param None
        :returns: a dictionary containing failure rates for each task/step in the following format::
                  {task: failure_rate}
        :rtype: dict
        """
        pass

    # Helper functions
    def filterWorkflowsByStatus(self, workflows, status):
        """
        :param list of Workflows
        :returns: workflows in the given status
        :rtype: list of Workflow objects
        """

        for workflow in workflows:
            if workflow.getRequestStatus() != status:
                workflows.remove(workflow)
        return workflows

    def removeRejectedWorkflows(self,workflows):
        """
        :param list of Workflows
        :returns: removes the inactive workflows in the given list and returns the updated list
        :rtype: list of Workflow objects
        """
        inactiveStates = ["aborted",
                          "aborted-archived",
                          "rejected",
                          "rejected-archived"]
        result = []
        for workflow in workflows:
            status = workflow.getRequestStatus()
            if status.lower() not in inactiveStates:
                result.append(workflow)
        return result

    # Write a unit test for this function
    def getYoungestWorkflow(self):
        """
        :param None
        :returns: returns the youngest workflow under given prepID
        :rtype: Workflow object
        """
        workflows = self.getWorkflows()
        activeWorkflows = self.removeRejectedWorkflows(workflows)
        return min(activeWorkflows, key=lambda x: x.getAge())
        
    def getPercentCompletions(self):
        return self.getOriginalWorkflow().getPercentCompletions()

    def getACDCs(self, valid=False):
        """
        :param: valid (optional), impose that the ACDC is workflow is in a valid state.
        :returns: Finds ACDCs.
        :type: list of Workflow objects.
        """
        workflows = self.getWorkflows()
        if valid: acdcs = self.removeRejectedWorkflows(workflows)
        return [w for w in workflows if 'acdc' in w.wf.lower()] if workflows is not None else []


    def getDuplicateACDCs(self):
        """
        :param: None
        :returns: Finds duplicate ACDCs, i.e. ACDCs that have the same initial task.
                  Returns a dictionary of duplicates tasks with each value is the list
                  of ACDCs that were made for that task
        :rtype: dict.
        """
        valid_acdcs = self.getACDCs(valid=True)

        # for each workflow, find the original task it was spawned from
        parent_tasks = [x.getParentTaskName() for x in valid_acdcs]

        # if any task has multiple ACDCs that weren't rejected, it's a duplicate
        parent_tasks_dict = defaultdict(list)
        for task, acdc in zip(parent_tasks, valid_acdcs):
            parent_tasks_dict[task].append(acdc)
        duplicates_dict = {task: list_of_acdcs for task, list_of_acdcs in parent_tasks_dict.items() if len(list_of_acdcs) > 1}

        # return list of duplicates
        return duplicates_dict


    def checkExistingACDC(self, initialTaskName):
        """
        :param: Task name you want to submit an ACDC for, and check if an ACDC already exists. str.
        :returns: True or False, i.e. whether a valid ACDC for this task already exists.
        :rtype: bool.
        """
        valid_acdcs = self.getACDCs(valid=True)
        parent_tasks = [x.getParentTaskName() for x in valid_acdcs]
        return initialTaskName in parent_tasks
