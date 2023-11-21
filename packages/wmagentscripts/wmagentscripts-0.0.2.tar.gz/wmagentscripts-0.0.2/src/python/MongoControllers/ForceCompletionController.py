import copy
from logging import Logger
from pymongo.collection import Collection

from Databases.Mongo.MongoClient import MongoClient


from typing import Optional, Any


class ForceCompletionController(MongoClient):
    """
    ForceCompletionController
    General API for logging the force completion requests
    """

    def __init__(self, logger: Optional[Logger] = None) -> None:
        try:
            super().__init__(logger=logger)
        except Exception as error:
            raise Exception(f"Error initializing ForceCompletionController\n{str(error)}")

    def _setMongoCollection(self) -> Collection:
        return self.client.unified.ForceCompletion

    def _buildMongoDocument(self, data) -> dict:
        return copy.deepcopy(data)
    
    def insert(self, data: Any, query: Optional[dict] = None) -> None:
        self._set(data, query=query)
    

    
    

