import unittest
from mock import patch
from io import StringIO
import sys
from collections import defaultdict
import re
import os

from fleague.league_ranker import process_results, rank_teams, read_input_file

# Some tests seem excessive, but better to expect any eventuality than just the common issues.
class TestResultProcessing(unittest.TestCase):

    def test_process_results_valid_input(self):
        results = "TeamA 3 TeamB 1, TeamC 2 TeamD 2"
        expected_points = defaultdict(int)
        expected_points['TeamA'] = 3
        expected_points['TeamB'] = 0
        expected_points['TeamC'] = 1
        expected_points['TeamD'] = 1
        self.assertEqual(process_results(results), expected_points)

    def test_process_results_draw(self):
        results = "TeamX 2 TeamY 2"
        expected_points = defaultdict(int)
        expected_points['TeamX'] = 1
        expected_points['TeamY'] = 1
        self.assertEqual(process_results(results), expected_points)

    def test_process_results_multiple_matches(self):
        results = "Alpha 1 Beta 0, Gamma 2 Delta 3, Alpha 0 Gamma 0"
        expected_points = defaultdict(int)
        expected_points['Alpha'] = 4
        expected_points['Beta'] = 0
        expected_points['Gamma'] = 2
        expected_points['Delta'] = 3
        self.assertEqual(process_results(results), expected_points)

    @patch('sys.exit')
    @patch('sys.stdout', new_callable=StringIO)
    def test_process_results_odd_number_of_teams(self, stdout_mock, exit_mock):
        results = "Team1 1"
        process_results(results)
        exit_mock.assert_called_once_with(1)
        self.assertIn("Error: Two teams are needed for each match.", stdout_mock.getvalue())

    @patch('sys.exit')
    @patch('sys.stdout', new_callable=StringIO)
    def test_process_results_same_team_competing(self, stdout_mock, exit_mock):
        results = "TeamA 2 TeamA 1"
        process_results(results)
        exit_mock.assert_called_once_with(1)
        self.assertIn("Error: TeamA cannot compete against itself.", stdout_mock.getvalue())

    def test_process_results_empty_input(self):
        results = ""
        expected_points = defaultdict(int)
        self.assertEqual(process_results(results), expected_points)

    def test_process_results_input_with_extra_comma(self):
        results = "TeamA 1 TeamB 0,"
        expected_points = defaultdict(int)
        expected_points['TeamA'] = 3
        expected_points['TeamB'] = 0
        self.assertEqual(process_results(results), expected_points)

class TestRankingTeams(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_rank_teams_single_winner(self, stdout_mock):
        points = {'TeamA': 3, 'TeamB': 0}
        rank_teams(points)
        expected_output = "1. TeamA, 3 pts\n2. TeamB, 0 pt\n"
        self.assertEqual(stdout_mock.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_rank_teams_with_tie(self, stdout_mock):
        points = {'TeamX': 1, 'TeamY': 1, 'TeamZ': 3}
        rank_teams(points)
        expected_output = "1. TeamZ, 3 pts\n2. TeamX, 1 pt\n2. TeamY, 1 pt\n"
        self.assertEqual(stdout_mock.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_rank_teams_multiple_ties(self, stdout_mock):
        points = {'A': 2, 'B': 2, 'C': 1, 'D': 1, 'E': 3}
        rank_teams(points)
        expected_output = "1. E, 3 pts\n2. A, 2 pts\n2. B, 2 pts\n4. C, 1 pt\n4. D, 1 pt\n"
        self.assertEqual(stdout_mock.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_rank_teams_alphabetical_tiebreaker(self, stdout_mock):
        points = {'TeamB': 3, 'TeamA': 3}
        rank_teams(points)
        expected_output = "1. TeamA, 3 pts\n1. TeamB, 3 pts\n"
        self.assertEqual(stdout_mock.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_rank_teams_empty_points(self, stdout_mock):
        points = {}
        rank_teams(points)
        self.assertEqual(stdout_mock.getvalue(), "")

class TestReadInputFile(unittest.TestCase):

    @patch('os.path.isfile', return_value=True)
    def test_read_input_file_success(self, isfile_mock):
        file_content = "Match 1 result, Match 2 result"
        with patch('builtins.open', unittest.mock.mock_open(read_data=file_content)) as mock_file:
            result = read_input_file("results.txt")
            self.assertEqual(result, file_content)
            mock_file.assert_called_once_with("results.txt", 'r', newline='', encoding='utf-8')
            isfile_mock.assert_called_once_with("results.txt")

    @patch('os.path.isfile', return_value=False)
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=StringIO)
    def test_read_input_file_not_found(self, stdout_mock, exit_mock, isfile_mock):
        read_input_file("non_existent_file.txt")
        exit_mock.assert_called_once_with(1)
        self.assertIn("Error: The file 'non_existent_file.txt' was not found.", stdout_mock.getvalue())
        isfile_mock.assert_called_once_with("non_existent_file.txt")

    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', side_effect=IOError("File access denied"))
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=StringIO)
    def test_read_input_file_io_error(self, stdout_mock, exit_mock, open_mock, isfile_mock):
        read_input_file("protected_file.txt")
        exit_mock.assert_called_once_with(1)
        self.assertIn("Error reading file 'protected_file.txt': File access denied", stdout_mock.getvalue())
        open_mock.assert_called_once_with("protected_file.txt", 'r', newline='', encoding='utf-8')
        isfile_mock.assert_called_once_with("protected_file.txt")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)