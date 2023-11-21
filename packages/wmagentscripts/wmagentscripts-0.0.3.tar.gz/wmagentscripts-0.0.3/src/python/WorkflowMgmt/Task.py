"""
File       : Task.py
Author     : Hasan Ozturk <haozturk AT cern dot com>
Description: Task class which provides all the information needed in task level.
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


class Task(CacheableBase):

    def __init__(self, taskName: str, workflow, logger: Optional[Logger] = None, **kwargs) -> None:
        """
        Initialize the Task class
        :param str taskName: is the name of the task
        :param workflow: name as a string or WorkflowController object
        """
        try:
            super(Task, self).__init__()
            self.logger = logger or getLogger(self.__class__.__name__)

            self.unifiedConfiguration = ConfigurationHandler("config/unifiedConfiguration.json")
            configurationHandler = ConfigurationHandler()

            self.taskName = taskName
            if type(workflow) == str:
                self.workflow = WorkflowController(workflow)
            else:
                self.workflow = workflow

        except Exception as error:
            raise Exception(f"Error initializing Task\n{str(error)}")

    def getWMErrorsSummary(self, getUnreported: bool =True) -> dict:
        """
        :param None
        :returns: a dictionary containing error codes in the following format::
              {step: {errorcode: {site: number_errors}}}
        :rtype: dict
        """
        return self.workflow.getWMErrorsSummary(getUnreported=getUnreported).get(self.taskName)

    def getFailureRate(self) -> dict:
        """
        :param None
        :returns: a float containing failure rate of the given task/step in the following format::
                  failure_rate
        :rtype: float
        """
        failureRate = self.workflow.getFailureRate()
        return failureRate.get(self.taskName)

    def getPrimaryAAA(self):
        """
        :param None
        :returns: if the primary AAA is on or off
        :rtype: bool
        """
        pass

    def getSecondaryAAA(self):
        """
        :param: None
        :returns: if the secondary AAA is on or off
        :rtype: bool
        """

        pass