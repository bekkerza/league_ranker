# Simple League Ranking Application

This Python script processes the results of a league's matches and displays the team rankings based on a simple point system.

## Features

* **Processes match results:** Takes a string of match results as input.
* **Calculates points:** Awards 3 points for a win, 0 for a loss, and 1 for a draw.
* **Handles multiple matches:** Can process results for several matches.
* **Error handling:** Checks for invalid input formats (odd number of teams, a team playing against itself, and file not found/read errors).
* **Ranks teams:** Sorts teams based on points (highest first) and then alphabetically for teams with the same number of points.
* **Displays rankings:** Prints the ranked list of teams with their total points.
* **Input from file or direct entry:** Can read match results from a specified file or accept them directly from the user.

## How to Use

1.  **Clone the project/repo:** git clone https://github.com/bekkerza/league_ranker.git and cd into it.

2.  **Run from the command line:**

    * **To provide input directly:**
        ```bash
        python league_ranker.py
        ```
        The script will then prompt you to "Enter match results: ". Enter the results in the format `"TeamA scoreA TeamB scoreB, TeamC scoreC TeamD scoreD, ..."` (separate matches with commas and team names and scores with spaces). For example:
        ```
        Enter match results: Lions 3 Tigers 1, Cheetahs 2 Leopards 2, Tigers 0 Cheetahs 4
        ```

    * **To provide input from a file:**
        Create a text file (e.g., `results.txt`) where each line contains the match results in the same format as above. For example:
        ```
        Lions 3 Tigers 1, Cheetahs 2 Leopards 2
        Tigers 0 Cheetahs 4, Leopards 1 Lions 1
        ```
        Then, run the script with the file path as a command-line argument:
        ```bash
        python league_ranker.py results.txt
        ```

3.  **View the rankings:** The script will print the league rankings to the console, showing the rank, team name, and total points. For example:
    ```
    1. Cheetahs, 7 pts
    2. Lions, 4 pts
    3. Leopards, 2 pts
    4. Tigers, 0 pt
    ```
    Teams with the same number of points will have the same rank and will be listed alphabetically.

## Input Format

The match results should be provided as a string where each match is represented by two teams and their scores, separated by a space. Multiple matches should be separated by commas.

**Example:**
TeamA 2 TeamB 1, TeamC 0 TeamD 0, TeamE 3 TeamF 2

## Error Handling

The script includes basic error handling for the following scenarios:

* **Odd number of teams:** If the input results in an odd number of team-score pairs, an error message will be printed, and the script will exit.
* **Team playing against itself:** If a match result shows the same team playing against itself, an error message will be printed, and the script will exit.
* **File not found:** If a file path is provided as an argument, but the file does not exist, an error message will be printed, and the script will exit.
* **Error reading file:** If there is an error while trying to read the specified file, an error message will be printed, and the script will exit.

## Dependencies

This script uses standard Python libraries and has no external dependencies, hence no requirements.txt file generated.
