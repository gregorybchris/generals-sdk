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


def get_cumulative_ranks_df(games, rolling_average_n=None):
    results = []
    rank_map = dict()
    for game_number, game in enumerate(games):
        # Update rankings
        for rank, player in enumerate(game.ranking):
            if player not in rank_map:
                rank_map[player] = []
            normalized_rank = rank / (len(game.ranking) - 1)
            rank_map[player].append(normalized_rank)

        for player, ranks in rank_map.items():
            discounted_ranks = ranks if rolling_average_n is None else ranks[-rolling_average_n:]
            result = {
                'Game Number': game_number,
                'Player': player,
                'Average Normalized Rank': sum(discounted_ranks) / len(discounted_ranks),
            }
            results.append(result)
    return pd.DataFrame(results)


def plot_cumulative_ranks(games, rolling_average_n=None):
    df = get_cumulative_ranks_df(games, rolling_average_n=rolling_average_n)
    sns.lineplot(x='Game Number', y='Average Normalized Rank', hue='Player', data=df)
    plt.show()


def get_1v1_encoded_df(games):
    players = list(set([player for game in games for player in game.ranking]))

    results = []
    for game in games:
        for winner_i in range(len(game.ranking)):
            for loser_i in range(winner_i + 1, len(game.ranking)):
                winner = game.ranking[winner_i]
                loser = game.ranking[loser_i]

                result = []
                for player in players:
                    if player == winner:
                        result.append(1)
                    elif player == loser:
                        result.append(-1)
                    else:
                        result.append(0)
                results.append(result)
    return pd.DataFrame(results, columns=players)


if __name__ == '__main__':
    # tracked_players = [Players.CHRIS, Players.HIROTO,
    #                    Players.JACK, Players.JASON, Players.JONATHAN,
    #                    Players.KEVIN, Players.LEXI, Players.MAX,
    #                    Players.MIKE, Players.ROBERT, Players.RYAN, Players.YUKI]
    tracked_players = [Players.CHRIS, Players.JASON, Players.YUKI,
                       Players.ROBERT, Players.KEVIN, Players.MAX,
                       Players.HIROTO]
    # tracked_players = [Players.CHRIS, Players.HIROTO, Players.MAX]
    # tracked_players = [Players.CHRIS, Players.KEVIN, Players.YUKI]
    # tracked_players = [Players.CHRIS, Players.MAX]

    game_factory = GameFactory(tracked_players, use_cache=True)
    games = game_factory.get_games(game_type=Game.TYPE_CUSTOM,
                                   all_in_game_players_tracked=False,
                                   all_tracked_players_in_game=False,
                                   filter_untracked=True)

    if len(games) == 0:
        raise ValueError("No games found matching filter criteria")

    print(f"Found {len(games)} games")
    for game in games:
        print(game)

    print_stats(games)
    rolling_average_n = len(games) // 10
    plot_cumulative_ranks(games, rolling_average_n=rolling_average_n)
