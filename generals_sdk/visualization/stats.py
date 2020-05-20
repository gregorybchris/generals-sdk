from trueskill import Rating, rate


def _print_sorted_dict(d, invert=False, title=None, key=None):
    if key is None:
        key = lambda x: x
    if title is not None:
        print('\n' + title)
    multiplier = -1 if invert else 1
    sorted_d = sorted(list(d.items()), key=lambda p: multiplier * key(p[1]))
    for k, v in sorted_d:
        print(f"  {k}: {v}")


def _get_trueskill(games):
    trueskill_ratings = dict()
    for game_number, game in enumerate(games):
        for player in game.ranking:
            if player not in trueskill_ratings:
                trueskill_ratings[player] = Rating()
        team_ratings = [[trueskill_ratings[player]] for player in game.ranking]
        team_ranks = list(range(len(game.ranking)))
        updated_team_ratings = rate(team_ratings, ranks=team_ranks)
        updated_ratings = dict(zip(game.ranking, [r[0] for r in updated_team_ratings]))
        trueskill_ratings.update(updated_ratings)
    ratings = {player: (rating.mu, rating.sigma) for player, rating in trueskill_ratings.items()}
    return ratings


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

    trueskill = _get_trueskill(games)
    _print_sorted_dict(trueskill, invert=True, title='TrueSkill Ratings', key=lambda p: p[0])
