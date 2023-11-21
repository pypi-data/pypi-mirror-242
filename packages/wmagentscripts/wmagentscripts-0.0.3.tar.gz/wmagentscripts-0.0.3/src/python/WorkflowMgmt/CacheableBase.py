"""
base class to handle cacheable object info

:authors: Daniel Abercrombie <dabercro@mit.edu>
"""

import os
import json
import time
import threading
from functools import wraps
from logging import Logger

from typing import Optional, Tuple, List, Union

from Utilities.ConfigurationHandler import ConfigurationHandler
from Utilities.Logging import getLogger

def cached_json(attribute, timeout=None):
    """
    A decorator for caching dictionaries in local files.

    :param str attribute: The key of the :py:class:`WorkflowInfo` cache to
                          set using the decorated function.
    :param int timeout: The amount of time before refreshing the JSON file, in seconds.
    :returns: Function decorator
    :rtype: func
    """

    def cache_decorator(func):
        """
        The actual decorator (since decorator takes an argument)

        :param func func: A function to modify
        :returns: Decorated function
        :rtype: func
        """

        @wraps(func)
        def function_wrapper(self, *args, **kwargs):
            """
            Executes the :py:class:`WorkflowInfo` function

            :returns: Output of the originally decorated function
            :rtype: dict
            """
            if not os.path.exists(self.cache_dir):
                os.mkdir(self.cache_dir)
                self.logger.info('created')

            cacheLastUpdateLimit = kwargs.get('cacheLastUpdateLimit')
            if cacheLastUpdateLimit is not None and type(cacheLastUpdateLimit) not in [float, int]:
                self.logger.error('cacheLastUpdateLimit should be float or int (seconds).')

            check_var = self.cache.get(attribute)
            if check_var is None:
                file_name = self.cache_filename(attribute)
                self.logger.info( attribute + " " + file_name )
                if os.path.exists(file_name):

                    # each cache entry has a built in, default timeout, so we need to check it
                    if timeout is None or time.time() - timeout < os.stat(file_name).st_mtime:
                        # if the function specifies a 'freshness requirement', respect it
                        if cacheLastUpdateLimit is None or time.time() - cacheLastUpdateLimit < os.stat(file_name).st_mtime:
                            try:
                                self.logger.info('using cached file %s' % file_name)
                                with open(file_name, 'r') as cache_file:
                                    check_var = json.load(cache_file)
                            except ValueError:
                                self.logger.error('JSON file no good. Deleting %s. Try again later.' % file_name)
                                os.remove(file_name)

                # If still None, call the wrapped function and make the cache
                if check_var is None:
                    self.logger.info( 'cached file not found or cached file not fresh enough' )
                    check_var = func(self, *args, **kwargs)
                    with open(file_name, 'w') as cache_file:
                        json.dump(check_var, cache_file)

                self.cache[attribute] = check_var

            return check_var or {}

        return function_wrapper

    return cache_decorator


class CacheableBase(object):
    """
    Implements shared operations on the cache
    """

    def __init__(self, logger: Optional[Logger] = None):
        # Stores things using the cached_json decorator
        self.cache = {}
        self.unifiedConfiguration = ConfigurationHandler("config/unifiedConfiguration.json")
        configurationHandler = ConfigurationHandler()
        self.cache_dir = configurationHandler.get("cache_dir")
        self.bak_dir = os.path.join(self.cache_dir, 'bak/')

        self.logger = logger or getLogger(self.__class__.__name__)

    def __str__(self):
        pass

    def cache_filename(self, attribute):
        """
        Return the name of the file for caching

        :param str attribute: The information to store in the file
        :returns: The full file name to store the cache
        :rtype: str
        """
        return os.path.join(self.cache_dir, '%s.%s' % (self, attribute))

    def reset(self):
        """
        Reset the cache for this object and clear out the files.
        """

        if not os.path.exists(self.bak_dir):
            os.mkdir(self.bak_dir)

        for file in os.listdir(self.cache_dir):
            if '%s' % (self) in file:
                file = os.path.join(self.cache_dir, file)
                os.rename(file, file.replace(self.cache_dir, self.bak_dir))
                self.logger.info("Resetting %s" % file)

        self.cache.clear()
        self.logger.info("Cache for %s has been reset" % self)