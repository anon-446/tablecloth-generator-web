import csv
import sys
import os
import json

input_file = sys.argv[1]
output_dir = sys.argv[2]

def process_team_config(team_to_players):
    team_config = {
        'teams': [],
        'players': {}
    }
    sorted_teams = sorted(team_to_players.keys(), key=int)

    for team in sorted_teams:
        team_name = 'Team' + team
        team_config['teams'].append(team_name)
        team_config['players'][team_name] = team_to_players[team]

    return team_config

def process_json():
    team_to_players = {}
    id_config = {}

    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            print(row)
            name = row['name']
            team = row['team']
            id = row['id']
            id_config[id] = team
            if team not in team_to_players:
                team_to_players[team] = []
            team_to_players[team].append(name)

    with open(os.path.join(output_dir, "id-teams.json"), 'w') as f:
        json.dump(id_config, f, indent=2)

    team_config = process_team_config(team_to_players)
    with open(os.path.join(output_dir, "teams.json"), 'w') as f:
        json.dump(team_config, f, indent=2)

if __name__ == "__main__":
    process_json()