import json
import os

import numpy as np


def main():
    with open('teams.json') as f:
        teams = json.load(f)

    output = {}

    for team_id, team in teams.items():
        for player in team['players']:
            player_id = player['account_id']
            with open(f'data/series/{player_id}.json') as f:
                series = json.load(f)
            wins = [
                row for row in series['rows'] if row['win']
            ]
            losses = [
                row for row in series['rows'] if not row['win']
            ]
            output[player_id] = {
                'name': player['name'],
                'win': {
                    'count': len(wins),
                },
                'loss': {
                    'count': len(losses),
                },
            }
            for key in [
                "fantasy_points",
                "kills",
                "deaths",
                "last_hits",
                "gold_per_min",
                "towers_killed",
                "roshans_killed",
                "teamfight_participation",
                "observers_placed",
                "camps_stacked",
                "rune_pickups",
                "firstblood_claimed",
                "stuns",
            ]:
                output[player_id]['win'][key] = {
                    'avg': np.mean([float(row[key]) for row in wins]),
                    'std': np.std([float(row[key]) for row in wins]),
                }
                output[player_id]['loss'][key] = {
                    'avg': np.mean([float(row[key]) for row in losses]),
                    'std': np.std([float(row[key]) for row in losses]),
                }

    dirname = 'data'
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(f'{dirname}/stats.json', 'w') as f:
        json.dump(output, f, indent=4)


if __name__ == '__main__':
    main()
