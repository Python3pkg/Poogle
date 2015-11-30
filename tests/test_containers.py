import os
import unittest

from bs4 import BeautifulSoup
from mock import mock

import poogle
from poogle import containers


class PoogleBaseTestCase(unittest.TestCase):

    @mock.patch('poogle.Poogle')
    def setUp(self, mock_poogle):

        self.html_dir = os.path.join(os.path.dirname(__file__), 'html')
        with open(os.path.join(self.html_dir, 'test.html'), "r") as f:
            self.html = f.read()

        self.mock_poogle = mock_poogle
        mock_poogle.strict = False

        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.results_page = containers.PoogleResultsPage(mock_poogle, self.soup)


class PoogleTestCase(PoogleBaseTestCase):

    @mock.patch('poogle.requests.get')
    def test_poogle_attributes(self, mock_get):

        mock_get_response = mock.Mock()
        mock_get_response.content = self.html
        mock_get.return_value = mock_get_response

        obj = poogle.Poogle('test', 10)

        self.assertEqual(obj._query, 'test')
        self.assertEqual(obj.query, 'test')
        self.assertEqual(obj._min_results, 10)
        self.assertEqual(obj._query_count, 1)
        self.assertEqual(obj.total_results, 2390000000)
        self.assertEqual(obj._current, 20)

        self.assertIsInstance(obj.last, containers.PoogleResultsPage)
        self.assertEqual(obj._results[0][0], 0)
        self.assertIsInstance(obj._results[0][1], containers.PoogleResultsPage)
        self.assertEqual(len(obj._results[0][1]), 20)

        self.assertFalse(obj.strict)
        self.assertFalse(obj._lazy)
        self.assertEqual(obj._pause, 0.5)


class PoogleResultsTestCase(PoogleBaseTestCase):

    def test_results_page_container_attributes(self):
        self.assertIs(self.results_page._poogle, self.mock_poogle)
        self.assertIs(self.results_page._soup, self.soup)

        self.assertEqual(self.results_page.count, 20)
        self.assertEqual(len(self.results_page.results), 20)
        self.assertEqual(len(self.results_page), 20)

        self.assertEqual(self.results_page.total_results, 2390000000)

        self.assertIsNone(self.results_page.prev_url)
        self.assertIsNotNone(self.results_page.next_url)

    def test_results_container_attributes(self):
        first = self.results_page.results[0]
        self.assertEqual(first.title, 'Speedtest.net by Ookla - The Global Broadband Speed Test')
        self.assertEqual(first.url, 'www.speedtest.net/')

        fifth = self.results_page.results[4]
        self.assertEqual(fifth.title, 'Personality test based on C. Jung and I. Briggs Myers type theory')
        self.assertEqual(fifth.url, 'www.humanmetrics.com/cgi-win/jtypes2.asp')

        last = self.results_page.results[-1]
        self.assertEqual(last.title, 'Test - The Political Compass')
        self.assertEqual(last.url, 'https://www.politicalcompass.org/test')
