import logging

import requests
from requests.utils import quote
from bs4 import BeautifulSoup

from poogle import errors
from poogle.containers import PoogleResultsPage


class Poogle(object):

    SEARCH_URL = 'https://www.google.com/search?q='

    def __init__(self, query, pages=1, strict=False):
        self._log = logging.getLogger('poogle')
        self._query = query
        self._search_url = self.SEARCH_URL + quote(query)
        self._total_results = 0
        self._results = []

        self.strict = strict

    def _execute_query(self, page_no=1):
        try:
            self._log.info('Executing search query: %s', self._search_url)
            results = requests.get(self._search_url)
            results.raise_for_status()
        except requests.RequestException as e:
            self._log.error('An error occurred when executing the search query: %s', e.message)
            raise errors.PoogleRequestError(e.message)

        soup = BeautifulSoup(results.content, 'html.parser')
        page = PoogleResultsPage(self, soup)

        if page_no == 1:
            self._total_results = page.total_results

        self._results.append((page_no, page))
