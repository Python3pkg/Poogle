import os
import unittest

try:
    from bs4 import BeautifulSoup
except ImportError:
    from beautifulsoup4 import BeautifulSoup
from mock import mock

import poogle
from poogle import containers, errors


class PoogleResultsPageTestCase(unittest.TestCase):

    @mock.patch('poogle.Poogle')
    def setUp(self, mock_poogle):

        self.html_dir = os.path.join(os.path.dirname(__file__), 'html')
        with open(os.path.join(self.html_dir, 'test.html'), "r") as f:
            html = f.read()

        self.mock_poogle = mock_poogle
        mock_poogle.strict = False

        self.soup = BeautifulSoup(html, 'html.parser')
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
