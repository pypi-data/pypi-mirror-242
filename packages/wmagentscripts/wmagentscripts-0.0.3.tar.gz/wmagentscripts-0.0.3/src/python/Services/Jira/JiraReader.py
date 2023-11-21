import time
import os
import jira
from logging import Logger
from typing import List, Optional, Union

from Utilities.WebTools import getResponse
from Utilities.Logging import getLogger
from Utilities.IteratorTools import mapKeys, filterKeys
from Utilities.Decorators import runWithRetries
from Utilities.ConfigurationHandler import ConfigurationHandler


class JiraReader(object):

    def __init__(self, logger: Optional[Logger] = None) -> None:
        try:
            super().__init__()
            self.logger = logger or getLogger(self.__class__.__name__)

            configurationHandler = ConfigurationHandler()
            self.jiraUrl = os.getenv("JIRA_URL", configurationHandler.get("jira_url"))
         
            self.pat = self.read_pat(os.getenv("JIRA_PAT_PATH", configurationHandler.get("jira_pat_path")))
            self.client = self.logIn(self.pat)

            if not self.client:
                raise Exception("No JIRA Connection!")

        except Exception as error:
            raise Exception(f"Error initializing JiraReader\n{str(error)}")

    def read_pat(self, pat_path: str) -> str:
        with open(pat_path, 'r') as f:
            pat = f.read().strip()
        return pat

    def logIn(self, pat: str):
        try:
            print(pat)
            return jira.JIRA('https://its.cern.ch/jira' , token_auth=pat)
        except Exception as e:
            print("Failed to log in to JIRA: ", str(e))

    def getTicketCreationTime(self, ticket):
        return ticket.fields.created

    def find(self, specifications: dict = {}):
        query = 'project=CMSCOMPPR'
        summary = specifications.get('prepID', specifications.get('summary', None))
        if summary:
            query += ' AND summary~"%s"' % summary

        if specifications.get('status', None):
            status = specifications['status']
            if status.startswith('!'):
                query += ' AND status != %s' % (status[1:])
            else:
                query += ' AND status = %s' % status

        if specifications.get('label', None):
            label = specifications['label']
            query += ' AND labels = %s' % label

        if specifications.get('text', None):
            string = specifications['text']
            query += ' AND text ~ "%s"' % string

        return self._find(query)

    def _find(self, query):
        return self.client.search_issues(query, maxResults=-1)