import unittest
from io import StringIO
from unittest.mock import patch
from fleague.league_ranker import process_results, rank_teams

class TestLeagueApp(unittest.TestCase):
    
    def test_process_results_valid_input(self):
        input_data = "Lions 3, Snakes 3 Tarantulas 1, FC Awesome 0 Lions 1, FC Awesome 1 Tarantulas 3, Snakes 1 Lions 4, Grouches 0"
        points = process_results(input_data)
        
        # Check that points are calculated correctly
        self.assertEqual(points['Lions'], 5)
        self.assertEqual(points['Snakes'], 1)
        self.assertEqual(points['Tarantulas'], 6)
        self.assertEqual(points['FC Awesome'], 1)
        self.assertEqual(points['Grouches'], 0)
        
    def test_invalid_match_format(self):
        # Odd number of matches, should trigger "two teams needed" check
        input_data = "Lions 3, Snakes 3 Tarantulas 1"
        with self.assertRaises(SystemExit):
            process_results(input_data)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_rank_teams(self, mock_stdout):
        points = {
            'Tarantulas': 6,
            'Lions': 5,
            'FC Awesome': 1,
            'Snakes': 1,
            'Grouches': 0
        }
        
        rank_teams(points)
        
        # Check if the ranking is printed correctly
        output = mock_stdout.getvalue().strip().split('\n')
        
        # Check the output format of rankings
        self.assertEqual(output[0], "1. Tarantulas, 6 pts")
        self.assertEqual(output[1], "2. Lions, 5 pts")
        self.assertEqual(output[2], "3. FC Awesome, 1 pt")
        self.assertEqual(output[3], "3. Snakes, 1 pt")
        self.assertEqual(output[4], "5. Grouches, 0 pts")

if __name__ == '__main__':
    unittest.main()
