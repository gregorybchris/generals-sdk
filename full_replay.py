from games.game import Game
from games.game_factory import GameFactory
from games.replay_factory import ReplayFactory
from players import Players


if __name__ == '__main__':
    tracked_players = [Players.CHRIS, Players.MAX]

    game_factory = GameFactory(tracked_players, use_cache=True)
    games = game_factory.get_games(game_type=Game.TYPE_CUSTOM,
                                   all_in_game_players_tracked=False,
                                   all_tracked_players_in_game=False,
                                   filter_untracked=True)

    print(f"Found {len(games)} games")
    for game in games:
        print(game)

    replay_factory = ReplayFactory()
    for game in games[-10:]:
        replay = replay_factory.get_replay(game)
        game.add_replay(replay)
        print(game.game_id, game.replay.generals, game.replay.width,
              game.replay.height, game.replay.usernames)
