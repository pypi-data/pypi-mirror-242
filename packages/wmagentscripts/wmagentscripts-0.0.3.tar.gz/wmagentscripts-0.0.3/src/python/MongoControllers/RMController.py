import copy
from logging import Logger
from pymongo.collection import Collection

from Databases.Mongo.MongoClient import MongoClient


from typing import Optional, Any


class RunningMonitorController(MongoClient):
    """
    __RunningMonitorController__
    General API for controlling the running-monitor stuck workflows info
    """

    def __init__(self, logger: Optional[Logger] = None) -> None:
        try:
            super().__init__(logger=logger)
        except Exception as error:
            raise Exception(f"Error initializing RunningMonitorController\n{str(error)}")

    def _setMongoCollection(self) -> Collection:
        return self.client.unified.RunningMonitor

    def _buildMongoDocument(self, data) -> dict:
        return copy.deepcopy(data)
    
    def insert(self, data: Any):
        self._set(data)
    
    def clear(self):
        self.collection.drop()

    
    

