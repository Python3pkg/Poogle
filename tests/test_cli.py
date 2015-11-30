import os
import unittest

import click
from bs4 import BeautifulSoup
from mock import mock
from click.testing import CliRunner

from poogle.cli import PoogleCLI, search


class PoogleCliTestCase(unittest.TestCase):

    def setUp(self):

        self.html_dir = os.path.join(os.path.dirname(__file__), 'html')
        with open(os.path.join(self.html_dir, 'test.html'), "r") as f:
            self.html = f.read()

        self.soup = BeautifulSoup(self.html, 'html.parser')


class PoogleHelpTestCase(PoogleCliTestCase):

    def test_poogle_cli(self):

        ctx_mock = mock.Mock()

        cli = PoogleCLI()
        self.assertListEqual(cli.list_commands(ctx_mock), ['search'])
        self.assertIsInstance(cli.get_command(ctx_mock, 'search'), click.core.Command)


class PoogleSearchTestCase(PoogleCliTestCase):

    @mock.patch('poogle.requests.get')
    def test_search(self, mock_get):

        mock_get_response = mock.Mock()
        mock_get_response.content = self.html
        mock_get.return_value = mock_get_response

        runner = CliRunner()
        result = runner.invoke(search.cli, ['-r 3', 'test'])

        self.assertEqual(result.exit_code, 0)
        expected_output = '''Executing search query for test

Speedtest.net by Ookla - The Global Broadband Speed Test
==============================
http://www.speedtest.net/

Test.com
==============================
https://www.test.com/

Test - Wikipedia, the free encyclopedia
==============================
https://en.wikipedia.org/wiki/Test

'''
        self.assertEqual(result.output, expected_output)

    @mock.patch('poogle.requests.get')
    def test_search_plain(self, mock_get):

        mock_get_response = mock.Mock()
        mock_get_response.content = self.html
        mock_get.return_value = mock_get_response

        runner = CliRunner()
        result = runner.invoke(search.cli, ['-r 3', '--plain', 'test'])

        self.assertEqual(result.exit_code, 0)
        expected_output = '''Executing search query for test

Speedtest.net by Ookla - The Global Broadband Speed Test
==============================
http://www.speedtest.net/

Test.com
==============================
https://www.test.com/

Test - Wikipedia, the free encyclopedia
==============================
https://en.wikipedia.org/wiki/Test

'''
        self.assertEqual(result.output, expected_output)

