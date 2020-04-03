import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from games.game import Game
from games.game_factory import GameFactory
from players import Players


sns.set()
sns.set_style('white')


def print_sorted_dict(d, invert=False, title=None):
    if title is not None:
        print('\n' + title)
    multiplier = -1 if invert else 1
    sorted_d = sorted(list(d.items()), key=lambda p: multiplier * p[1])
    for k, v in sorted_d:
        print(f"  {k}: {v}")


def print_stats(games):
    ranking_map = dict()
    for game in games:
        for rank, name in enumerate(game.ranking):
            if name not in ranking_map:
                ranking_map[name] = []
            ranking_map[name].append(rank / (len(game.ranking) - 1))

    n_games = {name: len(ranks) for name, ranks, in ranking_map.items()}
    print_sorted_dict(n_games, invert=True, title='Number of Games Played')

    average_ranks = {name: (sum(ranks) / len(ranks)) for name, ranks in ranking_map.items()}
    print_sorted_dict(average_ranks, title='Average Normalized Rank')

    fprw = {name: (sum([1 if rank == 0 else 0 for rank in ranks]) / len(ranks)) for name, ranks in ranking_map.items()}
    print_sorted_dict(fprw, invert=True, title='Average First Place Win Rate')


def get_cumulative_ranks_df(games):
    results = []
    rank_map = dict()
    for game_number, game in enumerate(games):
        # Update rankings
        for rank, player in enumerate(game.ranking):
            if player not in rank_map:
                rank_map[player] = []
            rank_map[player].append(rank / (len(game.ranking) - 1))

        for player, ranks in rank_map.items():
            result = {
                'Game Number': game_number,
                'Player': player,
                'Average Normalized Rank': sum(ranks) / len(ranks),
            }
            results.append(result)
    return pd.DataFrame(results)


def plot_cumulative_ranks(games):
    df = get_cumulative_ranks_df(games)
    sns.lineplot(x='Game Number', y='Average Normalized Rank', hue='Player', data=df)
    plt.show()


if __name__ == '__main__':
    tracked_players = [Players.CHRIS, Players.JASON, Players.YUKI,
                       Players.ROBERT, Players.KEVIN, Players.MAX]

    factory = GameFactory(tracked_players)
    games = factory.get_games(game_type=Game.TYPE_CUSTOM, use_cache=True)

    print_stats(games)
    plot_cumulative_ranks(games)
