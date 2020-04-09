def _print_sorted_dict(d, invert=False, title=None):
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
    _print_sorted_dict(n_games, invert=True, title='Number of Games Played')

    average_ranks = {name: (sum(ranks) / len(ranks)) for name, ranks in ranking_map.items()}
    _print_sorted_dict(average_ranks, title='Average Normalized Rank')

    fprw = {name: (sum([1 if rank == 0 else 0 for rank in ranks]) / len(ranks)) for name, ranks in ranking_map.items()}
    _print_sorted_dict(fprw, invert=True, title='Average First Place Win Rate')
