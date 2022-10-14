import json
import argparse
import random

import numpy as np


class Card:
    def __init__(self, card_id, card_bonuses, base_stats):
        self.id = card_id
        self.bonuses = card_bonuses
        self.stats = base_stats
        self.scores = []
        self._day_scores = []
        self._series_scores = []
        self._games_played = 0
        self._games_counted = 0
        self._series_played = 0

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
            if not args.no_bonus:
                roll *= 1 + (self.bonuses[key]/100)  # apply card bonus
            total += roll
        self._series_scores.append(total)

    def flush_series(self, best):
        counting_games = sorted(self._series_scores)[-best:]
        self._games_played += len(self._series_scores)
        self._games_counted += len(counting_games)
        self._series_played += 1
        self._day_scores.append(sum(counting_games))
        self._series_scores = []

    def flush_day(self):
        self.scores.append(max(self._day_scores))
        self._day_scores = []


class Player:
    def __init__(self, player_data):
        self.id = player_data['account_id']
        self.name = player_data['name']
        self.role = player_data['role']
        self.cards = [
            Card(card_id, card_bonuses, stats_dict[str(self.id)])
            for card_id, card_bonuses in player_data['cards'].items()
        ]

    def roll(self, win):
        for card in self.cards:
            card.roll(win)

    def flush_series(self, best):
        for card in self.cards:
            card.flush_series(best)

    def flush_day(self):
        for card in self.cards:
            card.flush_day()


class Team:
    def __init__(self, team_id, team_data):
        self.id = team_id
        self.name = team_data['name']
        self.players = [
            Player(player_data) for player_data in team_data['players']
        ]
        self.rating = ratings_dict[team_id]

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


def print_results(team_objs, role):
    results = []
    for team_id, team in team_objs.items():
        for player in team.players:
            for card in player.cards:
                if player.role == role:
                    results.append({
                        'name': player.name,
                        'team': team.name,
                        'role': player.role,
                        'card_id': card.id,
                        'mean': np.mean(card.scores),
                        'std': np.std(card.scores),
                        'ci5': np.percentile(card.scores, 5),
                        'ci95': np.percentile(card.scores, 95),
                        'min': np.min(card.scores),
                        'max': np.max(card.scores),
                        # 'series': card._series_played,
                        # 'games': card._games_played,
                        # 'counted': card._games_counted,
                    })
    print(
        f"{'NAME':<13s}",
        f"{'TEAM':<22}",
        f"{'ROLE':<8s}",
        f"{'CARD ID':<8s}",
        f"{'MEAN':<7s}",
        f"{'STD':<7s}",
        f"{'5% CI':<7s}",
        f"{'95% CI':<7s}",
        f"{'MIN':<7s}",
        f"{'MAX':<7s}",
        # f"{'SERIES':<7s}",
        # f"{'GAMES':<6s}",
        # f"{'COUNTED':<8s}",
    )
    print(
        f"{'-'*12:<13s}",
        f"{'-'*21:<22}",
        f"{'-'*7:<8s}",
        f"{'-'*7:<8s}",
        f"{'-'*6:<7s}",
        f"{'-'*6:<7s}",
        f"{'-'*6:<7s}",
        f"{'-'*6:<7s}",
        f"{'-'*6:<7s}",
        f"{'-'*6:<7s}",
        # f"{'-'*6:<7s}",
        # f"{'-'*6:<6s}",
        # f"{'-'*6:<8s}",
    )
    for i, result in enumerate(sorted(results, key=lambda v: v['mean'], reverse=True)):
        print(
            f"{result['name']:<13s}",
            f"{result['team']:<22}",
            f"{result['role']:<8s}",
            f"{result['card_id']:<8s}",
            f"{result['mean']:<7.2f}",
            f"{result['std']:<7.2f}",
            f"{result['ci5']:<7.2f}",
            f"{result['ci95']:<7.2f}",
            f"{result['min']:<7.2f}",
            f"{result['max']:<7.2f}",
            # f"{result['series']:<7d}",
            # f"{result['games']:<6d}",
            # f"{result['counted']:<8d}",
        )
        if args.top and ((role == 'Mid' and i == 4) or (i == 9)):
            break
    print('')


def main(args):
    # get games from schedule
    games = schedule_dict[args.day_number]

    # init teams
    team_objs = {
        team_id: Team(team_id, team_data)
        for team_id, team_data in teams_dict.items()
    }

    # main loop
    for i in range(args.n):
        if args.verbose and i % 10 == 0:
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
    print_results(team_objs, 'Mid')
    print_results(team_objs, 'Core')
    print_results(team_objs, 'Support')


if __name__ == '__main__':
    # load schedule
    with open('schedule.json') as f:
        schedule_dict = json.load(f)

    # load ratings
    with open('data/ratings.json') as f:
        ratings_dict = json.load(f)

    # load stats
    with open('data/stats.json') as f:
        stats_dict = json.load(f)

    # load teams
    with open('teams.json') as f:
        teams_dict = json.load(f)

    parser = argparse.ArgumentParser()
    parser.add_argument('day_number')
    parser.add_argument('-n', type=int, default=1000)
    parser.add_argument('--no-bonus', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--top', action='store_true')
    args = parser.parse_args()
    main(args)
