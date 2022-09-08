import requests
import logging
import json
import argparse
import os
import time


def request(url, params=None):
    r = requests.get(url, params=params)
    while r.status_code != 200:
        logging.debug('Rate limit exceeded, waiting 10 seconds')
        time.sleep(10)
        r = requests.get(url)
    time.sleep(1)
    return r.json()


def save(data, path):
    dirname = f'data/{os.path.dirname(path)}'
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(f'data/{path}', 'w') as f:
        json.dump(data, f, indent=4)


def get_ratings():
    output = {}
    for team_id, team in teams.items():
        url = f'https://api.opendota.com/api/teams/{team_id}'
        data = request(url)
        output[team_id] = data['rating']
    save(output, 'ratings.json')


def get_fantasy_series():
    for team_id, team in teams.items():
        for player in team['players']:
            get_player_fantasy_series(player)


def get_player_fantasy_series(player_data):
    player_id = player_data['account_id']
    leagues = player_data['leagues']
    sql = " ".join([
        "SELECT",
        ",".join([
            "round((0.3 * kills + (3 - 0.3 * deaths) + 0.003 * (last_hits + denies) + 0.002 * gold_per_min + towers_killed + roshans_killed + 3 * teamfight_participation + 0.5 * observers_placed + 0.5 * camps_stacked + 0.25 * rune_pickups + 4 * firstblood_claimed + 0.05 * stuns)::numeric, 1) fantasy_points",
            "round((0.3 * kills)::numeric, 1) kills",
            "round(((3 - 0.3 * deaths))::numeric, 1) deaths",
            "round((0.003 * (last_hits + denies))::numeric, 1) last_hits",
            "round((0.002 * gold_per_min)::numeric, 1) gold_per_min",
            "round((towers_killed)::numeric, 1) towers_killed",
            "round((roshans_killed)::numeric, 1) roshans_killed",
            "round((3 * teamfight_participation)::numeric, 1) teamfight_participation",
            "round((0.5 * observers_placed)::numeric, 1) observers_placed",
            "round((0.5 * camps_stacked)::numeric, 1) camps_stacked",
            "round((0.25 * rune_pickups)::numeric, 1) rune_pickups",
            "round((4 * firstblood_claimed)::numeric, 1) firstblood_claimed",
            "round((0.05 * stuns)::numeric, 1) stuns",
            "matches.match_id",
            "matches.start_time",
            "((player_matches.player_slot < 128) = matches.radiant_win) win",
            "player_matches.hero_id",
            "player_matches.account_id",
            "leagues.name leaguename",
        ]),
        "FROM matches",
        "JOIN match_patch using(match_id)",
        "JOIN leagues using(leagueid)",
        "JOIN player_matches using(match_id)",
        "JOIN heroes on heroes.id = player_matches.hero_id",
        "LEFT JOIN notable_players ON notable_players.account_id = player_matches.account_id",
        "LEFT JOIN teams using(team_id)",
        "WHERE TRUE",
        "AND round((0.3 * kills + (3 - 0.3 * deaths) + 0.003 * (last_hits + denies) + 0.002 * gold_per_min + towers_killed + roshans_killed + 3 * teamfight_participation + 0.5 * observers_placed + 0.5 * camps_stacked + 0.25 * rune_pickups + 4 * firstblood_claimed + 0.05 * stuns)::numeric, 1) IS NOT NULL",
        f"AND (player_matches.account_id = {player_id})",
        f"AND ({' OR '.join(f'matches.leagueid = {i}' for i in leagues)})",
    ])
    params = {
        'sql': sql,
    }
    url = "https://api.opendota.com/api/explorer"
    data = request(url, params=params)
    save(data, f'series/{player_id}.json')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # load teams
    with open('teams.json') as f:
        teams = json.load(f)

    # top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    # parser for "ratings" command
    parser_ratings = subparsers.add_parser('ratings')
    parser_ratings.set_defaults(func=get_ratings)

    # parser for "fantasy" command
    parser_ratings = subparsers.add_parser('fantasy')
    parser_ratings.set_defaults(func=get_fantasy_series)

    # parse arguments
    args = parser.parse_args()
    args.func()
