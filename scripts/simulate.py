import json
import argparse
import random

import numpy as np


class Player:
    def __init__(self, player_id, player_name):
        self.id = player_id
        self.name = player_name
        self.stats = stats[str(player_id)]
        self.scores = []
        self._day_scores = []
        self._series_scores = []

    def roll(self, win):
        total = 0
        for key in [
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
            if win:
                mean = self.stats['win'][key]['avg']
                std = self.stats['win'][key]['std']
            else:
                mean = self.stats['loss'][key]['avg']
                std = self.stats['loss'][key]['std']
            roll = np.random.normal(mean, std)
            if key != "deaths":  # only death score can be negative
                roll = max(roll, 0)
            total += roll
        self._series_scores.append(total)

    def flush_series(self, best):
        self._day_scores.append(sum(sorted(self._series_scores)[-best:]))
        self._series_scores = []

    def flush_day(self):
        self.scores.append(sum(self._day_scores))
        self._day_scores = []


class Team:
    def __init__(self, team_id, team_name):
        self.id = team_id
        self.name = team_name
        self.players = [
            Player(player['account_id'], player['name'])
            for player in teams[team_id]['players']
        ]
        self.rating = ratings[team_id]

    def roll(self, win):
        for player in self.players:
            player.roll(win)

    def flush_series(self, best):
        for player in self.players:
            player.flush_series(best)

    def flush_day(self):
        for player in self.players:
            player.flush_day()


class Series:
    def __init__(self, team_a, team_b, best_of):
        self.team_a = team_a
        self.team_b = team_b
        self.best_of = best_of
        self.win_prob = win_prob(self.team_a.rating, self.team_b.rating)
        self._results = []

    @property
    def team_a_wins(self):
        return sum(result for result in self._results if result)

    @property
    def team_b_wins(self):
        return sum(not result for result in self._results if not result)

    def roll(self):
        result = random.random() < self.win_prob
        self.team_a.roll(result)
        self.team_b.roll(not result)
        self._results.append(result)

    def is_over(self):
        assert self.team_a_wins <= self.best_of//2 + 1
        assert self.team_b_wins <= self.best_of//2 + 1
        assert self.team_a_wins + self.team_b_wins <= self.best_of
        if self.best_of == 3:
            if self.team_a_wins == 2 or self.team_b_wins == 2:
                return True
            else:
                return False
        elif self.best_of == 5:
            if self.team_a_wins == 3 or self.team_b_wins == 3:
                return True
            else:
                return False
        elif self.best_of == 2:
            return False
        else:
            raise ValueError(f'unrecognized best_of: {self.best_of}')

    def flush(self):
        best = self.best_of//2 + 1
        self.team_a.flush_series(best)
        self.team_b.flush_series(best)

    def run(self):
        for i in range(self.best_of):
            self.roll()
            if self.is_over():
                break
        self.flush()


def win_prob(team_a_rating, team_b_rating):
    q_a = 10**(team_a_rating/400)
    q_b = 10**(team_b_rating/400)
    return q_a/(q_a+q_b)


def main(args):
    # get games from schedule
    games = schedule[args.day_number]

    # init teams
    team_objs = {
        team_id: Team(team_id, team['name']) for team_id, team in teams.items()
    }

    # main loop
    for i in range(args.n):
        if i % 10 == 0:
            print(f'{i}/{args.n}')
        # simulate series
        for game in games:
            team_a = team_objs[str(game['team_a'])]
            team_b = team_objs[str(game['team_b'])]
            series = Series(team_a, team_b, game['best_of'])
            series.run()
        # store results
        for team_id, team in team_objs.items():
            team.flush_day()

    # print results
    results = []
    for team_id, team in team_objs.items():
        for player in team.players:
            results.append({
                'name': player.name,
                'mean': np.mean(player.scores),
                'std': np.std(player.scores),
                'ci5': np.percentile(player.scores, 5),
                'ci95': np.percentile(player.scores, 95),
                'min': np.min(player.scores),
                'max': np.max(player.scores),
            })
    print(
        f"{'NAME':<14s}",
        f"{'MEAN':<10s}",
        f"{'STD':<10s}",
        f"{'5% CI':<10s}",
        f"{'95% CI':<10s}",
        f"{'MIN':<10s}",
        f"{'MAX':<10s}",
    )
    print(
        f"{'-'*13:<14s}",
        f"{'-'*9:<10s}",
        f"{'-'*9:<10s}",
        f"{'-'*9:<10s}",
        f"{'-'*9:<10s}",
        f"{'-'*9:<10s}",
        f"{'-'*9:<10s}",
    )
    for result in sorted(results, key=lambda v: v['mean'], reverse=True):
        print(
            f"{result['name']:<14s}",
            f"{result['mean']:<10.2f}",
            f"{result['std']:<10.2f}",
            f"{result['ci5']:<10.2f}",
            f"{result['ci95']:<10.2f}",
            f"{result['min']:<10.2f}",
            f"{result['max']:<10.2f}",
        )


if __name__ == '__main__':
    # load schedule
    with open('schedule.json') as f:
        schedule = json.load(f)

    # load ratings
    with open('data/ratings.json') as f:
        ratings = json.load(f)

    # load stats
    with open('data/stats.json') as f:
        stats = json.load(f)

    # load teams
    with open('teams.json') as f:
        teams = json.load(f)

    parser = argparse.ArgumentParser()
    parser.add_argument('day_number')
    parser.add_argument('-n', type=int, default=1000)
    args = parser.parse_args()
    main(args)
