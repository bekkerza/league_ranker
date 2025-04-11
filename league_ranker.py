import sys
import os
import re
from collections import defaultdict

def process_results(results):
    # Store points for each team
    points = defaultdict(int)

    # Use regex to find matches: each match is 'team score'
    matches = re.findall(r'(\w+ \d+)', results)

    # Ensure there are at least two teams for each match
    if len(matches) % 2 != 0:
        print("Error: Two teams are needed for each match. One team found without its opponent.")
        sys.exit(1)

    # Process each match pair - was tricky to build pairs on static pattern
    for i in range(0, len(matches), 2):
        # Extract teams and their scores
        team1, score1 = matches[i].split()
        team2, score2 = matches[i + 1].split()

        score1, score2 = int(score1), int(score2)

        # Ensure that teams are different, Lions can't play themselves and win, would be unfair ;-) 
        if team1 == team2:
            print(f"Error: {team1} cannot compete against itself.")
            sys.exit(1)

        # Update points based on the match results, a Lose = 0 by default, no need to calc it.
        if score1 > score2:
            points[team1] += 3  # Team 1 wins
        elif score2 > score1:
            points[team2] += 3  # Team 2 wins
        else:
            points[team1] += 1  # Draw
            points[team2] += 1

    return points

def rank_teams(points):
    # Sort by points (desc), and in case of a tie, alphabetically
    sorted_teams = sorted(points.items(), key=lambda x: (-x[1], x[0]))

    rank = 1
    current_points = None
    last_rank = None
    for idx, (team, team_points) in enumerate(sorted_teams):
        # Handle ranking teams with the same points
        if current_points is None or team_points != current_points:
            current_points = team_points
            rank = idx + 1
        # In case of tie, print same rank for teams
        if last_rank == rank:
            print(f"{rank}. {team}, {team_points} pts")
        else:
            print(f"{rank}. {team}, {team_points} pt{'s' if team_points > 1 else ''}")
        last_rank = rank

def read_input_file(file_path):
    # Use os.path to ensure platform-agnostic file handling, for Windows/Mac support
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if a file path is provided as a command-line argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        input_data = read_input_file(file_path)
    else:
        # If no file is provided, prompt for direct input
        input_data = input("Enter match results: ")

    # Process results and calculate points
    points = process_results(input_data)

    # Finallyu display rankings
    rank_teams(points)
