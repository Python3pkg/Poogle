import os
import unittest

import yurl
from bs4 import BeautifulSoup
from mock import mock
from poogle.errors import PoogleRequestError
from requests import RequestException

import poogle
from poogle import containers


class PoogleBaseTestCase(unittest.TestCase):

    def setUp(self):

        self.html_dir = os.path.join(os.path.dirname(__file__), 'html')
        with open(os.path.join(self.html_dir, 'test.html'), "r") as f:
            self.html = f.read()

        self.soup = BeautifulSoup(self.html, 'html.parser')


class PoogleTestCase(PoogleBaseTestCase):

    @mock.patch('poogle.requests.get')
    def test_poogle_attributes(self, mock_get):

        mock_get_response = mock.Mock()
        mock_get_response.content = self.html
        mock_get.return_value = mock_get_response

        obj = poogle.Poogle('test')
        self.assertEqual(repr(obj), "<Poogle Search: 'test'>")

        # Per page
        with self.assertRaises(ValueError):
            obj.per_page = 101

        with self.assertRaises(ValueError):
            obj.per_page = -1

        obj.per_page = 20

        self.assertIsInstance(obj.next_page(), containers.PoogleResultsPage)

        with self.assertRaises(AttributeError):
            obj.per_page = 30

        # Attributes
        self.assertEqual(obj._query, 'test')
        self.assertEqual(obj.query, 'test')
        self.assertEqual(obj.per_page, obj._per_page)
        self.assertEqual(obj._per_page, 20)
        self.assertEqual(obj._query_count, 1)
        self.assertEqual(obj.total_results, 2390000000)
        self.assertEqual(obj._current_page, 1)

        self.assertIsInstance(obj.last, containers.PoogleResultsPage)
        self.assertEqual(obj._results[0][0], 1)
        self.assertIsInstance(obj._results[0][1], containers.PoogleResultsPage)
        self.assertEqual(len(obj.results), 20)
        self.assertEqual(len(obj._results[0][1]), 20)

        self.assertFalse(obj.strict)
        self.assertTrue(obj._lazy)

        # Next page
        self.assertIsInstance(obj.next_page(), containers.PoogleResultsPage)
        self.assertEqual(len(obj.results), 40)
        self.assertEqual(len(obj._results), 2)
        self.assertEqual(obj._results[1][0], 2)

    @mock.patch('poogle.requests.get')
    @mock.patch.object(poogle.Poogle, 'next_page')
    def test_poogle_eager_loading(self, mock_next_page, mock_get):

        mock_get_response = mock.Mock()
        mock_get_response.content = self.html
        mock_get.return_value = mock_get_response

        obj = poogle.Poogle('test', 20, lazy=False)
        mock_next_page.assert_called_once_with()

    @mock.patch('poogle.requests.get')
    @mock.patch.object(poogle.Poogle, 'next_page')
    def test_poogle_lazy_loading(self, mock_next_page, mock_get):

        mock_get_response = mock.Mock()
        mock_get_response.content = self.html
        mock_get.return_value = mock_get_response

        obj = poogle.Poogle('test', 20, lazy=True)
        results = obj.results
        mock_next_page.assert_called_once_with()


    @mock.patch('poogle.requests.get')
    def test_poogle_bad_arguments(self, mock_get):

        mock_get_response = mock.Mock()
        mock_get_response.content = self.html
        mock_get.return_value = mock_get_response

        self.assertRaises(ValueError, poogle.Poogle, 'test', 101)
        self.assertRaises(ValueError, poogle.Poogle, 'test', -1)

    @mock.patch('poogle.requests.get')
    def test_request_error(self, mock_get):

        mock_get.side_effect = RequestException()
        self.assertRaises(PoogleRequestError, poogle.Poogle, 'test', 20, lazy=False)


class PoogleResultsTestCase(PoogleBaseTestCase):

    @mock.patch('poogle.Poogle')
    def setUp(self, mock_poogle):
        PoogleBaseTestCase.setUp(self)
        self.mock_poogle = mock_poogle
        self.results_page = containers.PoogleResultsPage(mock_poogle, self.soup)

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
        self.assertIsInstance(first.url, yurl.URL)
        self.assertEqual(first.url.as_string(), 'http://www.speedtest.net/')

        fifth = self.results_page.results[4]
        self.assertEqual(fifth.title, 'Personality test based on C. Jung and I. Briggs Myers type theory')
        self.assertIsInstance(fifth.url, yurl.URL)
        self.assertEqual(fifth.url.as_string(), 'http://www.humanmetrics.com/cgi-win/jtypes2.asp')

        last = self.results_page.results[-1]
        self.assertEqual(last.title, 'Test - The Political Compass')
        self.assertIsInstance(last.url, yurl.URL)
        self.assertEqual(last.url.as_string(), 'https://www.politicalcompass.org/test')


class PoogleGoogleSearchTestCase(PoogleBaseTestCase):

    @mock.patch('poogle.requests.get')
    @mock.patch('poogle.sleep')
    def test_standard_calls(self, mock_sleep, mock_get):

        mock_get_response = mock.Mock()
        mock_get_response.content = self.html
        mock_get.return_value = mock_get_response

        results = poogle.google_search('test query')
        self.assertEqual(len(results), 10)

        results = poogle.google_search('test query', 20)
        self.assertEqual(len(results), 20)

        mock_sleep.assert_not_called()

    # TODO: We need a large sample to test this with
    # @mock.patch('poogle.requests.get')
    # @mock.patch('poogle.sleep')
    # def test_large_calls(self, mock_sleep, mock_get):
    #
    #     mock_get_response = mock.Mock()
    #     mock_get_response.content = self.html
    #     mock_get.return_value = mock_get_response
    #
    #     results = poogle.google_search('test query', 150, 0.1)
    #     self.assertEqual(len(results), 150)
    #     mock_sleep.assert_called_once_with(0.1)

