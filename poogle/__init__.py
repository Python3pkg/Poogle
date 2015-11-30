import logging
from time import sleep

import requests
from requests.utils import quote
from bs4 import BeautifulSoup

from poogle.errors import PoogleMaxQueriesError, PoogleRequestError, PoogleNoMoreResultsError
from poogle.containers import PoogleResultsPage

__author__     = "Makoto Fujimoto"
__copyright__  = 'Copyright 2015, Makoto Fujimoto'
__license__    = "MIT"
__version__    = "0.1"
__maintainer__ = "Makoto Fujimoto"


class Poogle(object):

    SEARCH_URL = 'https://www.google.com/search?q='

    def __init__(self, query, min_results=10, max_queries=10, **kwargs):
        """
        Args:
            query(str):         The search query.
            min_results(int):   Minimum results only guarantees a *minimum*, it may return more results than requested.
            max_queries(int):   This should be set to protect against infinite loops. You can only request up to 100
                results per single query, so if you're trying to pull more than 1,000 results at once, you'll need to
                adjust this accordingly.
            **kwargs:           Arbitrary keyword arguments, refer to the online documentation for more information.
        """
        self._log = logging.getLogger('poogle')

        self._query        = query
        self._search_url   = self.SEARCH_URL + quote(query)

        self._min_results  = min_results
        self.max_queries   = max_queries
        self._query_count  = 0
        self.total_results = 0

        self._results      = []
        self._current      = 0
        self.last          = None

        self.strict = kwargs.get('strict', False)
        self._lazy  = kwargs.get('lazy', False)
        self._pause = kwargs.get('pause', 0.5)

        # Execute search queries until we have retrieved the minimum number of required results (unless querying lazily)
        if not self._lazy:
            self._get_minimum_results()

    def _get_minimum_results(self):
        """
        Begin query iteration until we have the minimum number of queries returned
        """
        while self._current < self._min_results:
            # If this is not our first query and we have a pause defined, wait here
            if self._current and self._pause:
                self._log.debug('Pausing for %s seconds between queries', self._pause)
                sleep(self._pause)

            try:
                self._execute_initial_queries()
            except PoogleNoMoreResultsError:
                break

    def _execute_initial_queries(self):
        """
        Execute the initial search queries

        Raises:
            PoogleRequestError: Raised if a search query can not be processed for any reason.
        """
        if self.max_queries is not None and self._query_count >= self.max_queries:
            raise PoogleMaxQueriesError

        # Set the number of search results to fetch
        num = min((self._min_results - self._current), 100)
        if not self._current:
            num += 10

        # Get the current search query URL
        if self._current:
            if not self.last.next_url:
                self._log.info('No more results to fetch')
                raise PoogleNoMoreResultsError('No more results to fetch')
            base_url = self.last.next_url
        else:
            base_url = self._search_url

        url = '{url}&num={n}'.format(url=base_url, n=num)

        # Execute the search query
        try:
            self._log.info('Executing first search query: %s', url)
            results = requests.get(url)
            results.raise_for_status()
        except requests.RequestException as e:
            self._log.error('An error occurred when executing the search query: %s', e.message)
            raise PoogleRequestError(e.message)

        # Parse the search results page
        soup = BeautifulSoup(results.content, 'html.parser')
        page = PoogleResultsPage(self, soup)
        self.total_results = page.total_results

        self._results.append((self._current, page))
        self._current += len(page)
        self._query_count += 1
        self.last = page

    def get_next(self, results=10):
        """
        Get the next <results> search results

        Args:
            results(int):   The number of additional search results to request. This has a cap limit of 100 per call.

        Returns:
            list[poogle.containers.PoogleResult]
        """
        if not self.last.next_url:
            raise PoogleNoMoreResultsError('There are no more search results available')

        url = '{url}&num={n}'.format(url=self.last.next_url, n=results)
        self._log.info('Executing supplemental search query: %s', url)

        # Execute the search query
        try:
            results = requests.get(url)
            results.raise_for_status()
        except requests.RequestException as e:
            self._log.error('An error occurred when executing the search query: %s', e.message)
            raise PoogleRequestError(e.message)

        # Parse the search results page
        soup = BeautifulSoup(results.content, 'html.parser')
        page = PoogleResultsPage(self, soup)
        self.total_results = page.total_results

        self._results.append((self._current, page))
        self._current += len(page)
        self.last = page

        return page.results

    @property
    def query(self):
        return self._query

    @property
    def results(self):
        """
        Concatenate results from all pages together and return

        Returns:
            list[poogle.containers.PoogleResult]
        """
        # If we're querying lazily, make sure we've fetched our initial results
        if self._lazy and not self._current:
            self._get_minimum_results()

        # Concatenate results from all pages together and return
        all_results = []
        for __, r in self._results:
            all_results += r.results

        return all_results

    def __repr__(self):
        return '<Poogle Search: "{q}">'.format(q=self._query)


def google_search(query, results=10):
    max_queries = int(results / 100) + 10
    poogle = Poogle(query, results, max_queries)

    return poogle.results[:results]
