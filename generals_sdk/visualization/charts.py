import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


sns.set()
sns.set_style('white')


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


def _get_1v1_encoded_df(games):
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
