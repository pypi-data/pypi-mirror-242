from time import struct_time, gmtime, mktime, asctime
from pymongo.collection import Collection
from jinja2 import Template
from logging import Logger
from Utilities.ConfigurationHandler import ConfigurationHandler
from Utilities.IteratorTools import mapKeys, mapKeysRecursive, mapValues
from Databases.Mongo.MongoClient import MongoClient
from Services.DBS.DBSReader import DBSReader

from typing import Any, Optional


class AssistanceController(MongoClient):
    """
    __AssistanceController__
    General API for reporting the workflows info
    """

    def __init__(self, logger: Optional[Logger] = None) -> None:
        try:
            super().__init__(logger=logger)
            self.template = {'errorReport': 'templates/AssistanceController/ErrorReport.jinja'}
            self.unifiedConfiguration = ConfigurationHandler(
                "config/unifiedConfiguration.json"
            )
            self.dbsReader = DBSReader()

        except Exception as error:
            raise Exception(f"Error initializing MongoClient\n{str(error)}")

    def _setMongoCollection(self) -> Collection:
        return self.client.unified.assistanceInfo



    def _convertValues(self, value: Any) -> Any:
        """
        The function to convert Mongo document values to required types
        :param value: value
        :return: converted value
        """
        return (
            list(value)
            if isinstance(value, set)
            else mapValues(self._convertValues, value)
            if isinstance(value, dict)
            else value
        )

    def _buildMongoDocument(self, data: dict, now: struct_time = gmtime()) -> dict:
        """
        This function is called by _set(), and rebuilds the document before we set it
        in the database.
        :data: the new data to be added to the workflow document
        :returns: the new document
        """
        data.update({"time": int(mktime(now)), "date": asctime(now)})
        data = mapKeysRecursive(lambda x: x.replace(".", "__dot__"), data)
        data = mapValues(self._convertValues, data)

        document = self.get(data.get("workflow")) or {}

        if document:
            document.setdefault("tasks", {})
            tasks_info = data.pop("tasks", {})

            # we update only the tasks that are in the incoming data
            for task in tasks_info.keys():
                existing_task_info = document["tasks"].get(task, None)
                new_task_info = tasks_info.get(task)

                # we update only the keys of each task dictionary that are present in the incoming data
                if existing_task_info:
                    task_info = existing_task_info.copy()
                    task_info.update(new_task_info)
                else:
                    task_info = new_task_info

                document["tasks"].update({task: task_info})

        document.update(data)
        return document

    def set(self, data: dict) -> None:
        """
        The function to set new data in the assistance info
        :param data: assistance data
        """
        try:
            super()._set(data, workflow=data.get("workflow"))

        except Exception as error:
            self.logger.error("Failed to set assistance info")
            self.logger.error(str(error))

    def setWorkflowIO(self, wf: str, IO: dict) -> None:
        """
        The function to set IO data in the assistance info of a given workflow
        :param wf: workflow name
        :param IO: IO data
        """
        self.set({**{"workflow": wf}, **IO})

    def setWorkflowPrepID(self, wf: str, prep_id: dict) -> None:
        """
        The function to set prep_id data in the assistance info of a given workflow
        :param wf: workflow name
        :param prep_id: prep_id data
        """
        self.set({"workflow": wf, "prep_id": prep_id})

    def setWorkflowPrimary(self, wf: str, primary: list) -> None:
        """
        The function to set primary data in the assistance info of a given workflow
        :param wf: workflow name
        :param primary: primary data
        """
        self.set({"workflow": wf, "primary": primary})

    def setWorkflowSecondary(self, wf: str, secondary: list) -> None:
        """
        The function to set secondary data in the assistance info of a given workflow
        :param wf: workflow name
        :param secondary: secondary data
        """
        self.set({"workflow": wf, "secondary": secondary})

    def setWorkflowOutputDatasets(self, wf: str, output_datasets: list) -> None:
        """
        The function to set output_datasets data in the assistance info of a given workflow
        :param wf: workflow name
        :param output_datasets: output_datasets data
        """
        self.set({"workflow": wf, "output_datasets": output_datasets})

    def setWorkflowRequestType(self, wf: str, req_type: dict) -> None:
        """
        The function to set req_type data in the assistance info of a given workflow
        :param wf: workflow name
        :param req_type: req_type data
        """
        self.set({"workflow": wf, "request_type": req_type})

    def setWorkflowPrepIDs(self, wf: str, prep_ids: dict) -> None:
        """
        The function to set prep_ids data in the assistance info of a given workflow
        :param wf: workflow name
        :param prep_ids: prep_ids data
        """
        self.set({"workflow": wf, "prep_ids": prep_ids})

    def setWorkflowPercentCompletions(self, wf: str, percent_completions: dict) -> None:
        """
        The function to set percent_completions data in the assistance info of a given workflow
        :param wf: workflow name
        :param percent_completions: percent_completions data
        """
        self.set({"workflow": wf, "percent_completions": percent_completions})

    def setWorkflowReqMgrStatus(self, wf: str, status: dict) -> None:
        """
        The function to set status data in the assistance info of a given workflow
        :param wf: workflow name
        :param status: status data
        """
        self.set({"workflow": wf, "reqmgr_status": status})

    def setWorkflowUnifiedStatus(self, wf: str, status: dict) -> None:
        """
        The function to set status data in the assistance info of a given workflow
        :param wf: workflow name
        :param status: status data
        """
        self.set({"workflow": wf, "unified_status": status})

    def setWorkflowLabels(self, wf: str, labels: dict) -> None:
        """
        The function to set labels data in the assistance info of a given workflow
        :param wf: workflow name
        :param labels: labels data
        """
        self.set({"workflow": wf, "labels": labels})

    def setWorkflowTask(self, wf: str, task: str, data: dict) -> None:
        """
        The function to set task data in the assistance info of a given workflow
        :param wf: workflow name
        :param taks: task name
        :param data: task data
        """
        self.set({"workflow": wf, "tasks": {task.split("/")[-1]: data}})

    def setWorkflowErrors(self, wf: str, task: str, errors: dict) -> None:
        """
        The function to set errors data in the assistance info of a given workflow
        :param wf: workflow name
        :param task: task name
        :param errors: errors data
        """
        self.setWorkflowTask(wf, task, {"errors": errors})

    def setWorkflowFilterEfficiency(self, wf: str, task: str, filter_efficiency: dict) -> None:
        """
        The function to set filter_efficiency data in the assistance info of a given workflow
        :param wf: workflow name
        :param task: task name
        :param filter_efficiency: filter_efficiency data
        """
        self.setWorkflowTask(wf, task, {"filter_efficiency": filter_efficiency})

    def setWorkflowLogs(self, wf: str, task: str, logs: dict) -> None:
        """
        The function to set logs data in the assistance info of a given workflow
        :param wf: workflow name
        :param task: task name
        :param logs: logs data
        """
        self.setWorkflowTask(wf, task, {"logs": logs})

    def setWorkflowBlocks(self, wf: str, task: str, blocks: dict) -> None:
        """
        The function to set blocks data in the assistance info of a given workflow
        :param wf: workflow name
        :param task: task name
        :param blocks: blocks data
        """
        self.setWorkflowTask(wf, task, {"needed_blocks": blocks})

    def setWorkflowFailureRate(self, wf: str, task: str, failure_rate: dict) -> None:
        """
        The function to set failure_rate data in the assistance info of a given workflow
        :param wf: workflow name
        :param task: task name
        :param failure_rate: failure_rate data
        """
        self.setWorkflowTask(wf, task, {"failure_rate": failure_rate})

    def setWorkflowJobStats(self, wf: str, task: str, job_stats: dict) -> None:
        """
        The function to set job_stats data in the assistance info of a given workflow
        :param wf: workflow name
        :param task: task name
        :param job_stats: job_stats data
        """
        self.setWorkflowTask(wf, task, {"job_stats": job_stats})

    def setWorkflowCampaign(self, wf: str, task: str, campaign: dict) -> None:
        """
        The function to set campaign data in the assistance info of a given workflow
        :param wf: workflow name
        :param task: task name
        :param campaign: campaign data
        """
        self.setWorkflowTask(wf, task, {"campaign": campaign})

    def setWorkflowFiles(self, wf: str, task: str, files: dict) -> None:
        """
        The function to set files data in the assistance info of a given workflow
        :param wf: workflow name
        :param task: task name
        :param files: files data
        """
        self.setWorkflowTask(wf, task, {"files": files})

    def setWorkflowUFiles(self, wf: str, task: str, ufiles: dict) -> None:
        """
        The function to set ufiles data in the assistance info of a given workflow
        :param wf: workflow name
        :param task: task name
        :param uFiles: ufiles data
        """
        self.setWorkflowTask(wf, task, {"ufiles": ufiles})

    def setWorkflowNUFiles(self, wf: str, task: str, nufiles: dict) -> None:
        """
        The function to set nufiles data in the assistance info of a given workflow
        :param wf: workflow name
        :param task: task name
        :param nufiles: nufiles data
        """
        self.setWorkflowTask(wf, task, {"n_ufiles": nufiles})

    def setWorkflowMissing(self, wf: str, task: str, missing: dict) -> None:
        """
        The function to set missing data in the assistance info of a given workflow
        :param wf: workflow name
        :param task: task name
        :param missing: missing data
        """
        self.setWorkflowTask(wf, task, {"missing": missing})

    def setWorkflowLogs(self, wf: str, task: str, logs: dict) -> None:
        """
        The function to set logging data in the assistance info of a given workflow
        :param wf: workflow name
        :param task: task name
        :param logs: logging data
        """
        self.setWorkflowTask(wf, task, {"logs": logs})

    def get(self, wf: str) -> dict:
        """
        The function to get the assistance info for a given workflow
        :param wf: workflow name
        :return: assistance info
        """
        try:
            return super()._getOne(dropParams=["_id"], workflow=wf)

        except Exception as error:
            self.logger.error("Failed to get the assistance info for workflow %s", wf)
            self.logger.error(str(error))

    def clean(self) -> None:
        """
        The function to delete all assistance info
        """
        try:
            super()._clean()

        except Exception as error:
            self.logger.error("Failed to clean all assistance info")
            self.logger.error(str(error))

    def cleanWorkflow(self, wf: str) -> None:
        """
        The function to delete all assistance info for a given workflow
        :param wf: workflow name
        """
        try:
            super()._clean(workflow=wf)

        except Exception as error:
            self.logger.error("Failed to clean the assistance info for workflow %s", wf)
            self.logger.error(str(error))

    def purge(self, expiredDays: int = 30) -> None:
        """
        The function to delete all assistance info if it is expired
        :param expiredDays: passed days from expiration time so that data can be deleted
        """
        try:
            super()._purge("time", expiredDays)

        except Exception as error:
            self.logger.error("Failed to purge assistance info expired for more than %s days", expiredDays)
            self.logger.error(str(error))

    def _renderErrorReportHTML(self, workflowName: str) -> str:
        """
        The function to render the error report HTML for one workflow.
        We read in the serialized workflow from mongoDB, and use the jinja template
        to construct the HTML report of errors.
        :param workflowName: string name of the workflow
        :return: str template
        """
        wf = self.get(workflowName)

        with open(self.template["errorReport"], "r") as tmpl:
            template = Template(tmpl.read())
            
        return template.render(
            time=asctime(gmtime()),
            wfn=workflowName,
            wf=wf,
            unifiedConfiguration=self.unifiedConfiguration,
            getDatasetEventsPerLumi=self.dbsReader.getDatasetEventsPerLumi,
        )


