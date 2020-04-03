import hashlib
import json
import os
import requests

from datetime import datetime

from .game import Game


class _GameConstants:
    _ID = 'id'
    _TYPE = 'type'
    _START_TIME = 'started'
    _TURNS = 'turns'
    _RANKING = 'ranking'
    _USERNAME = 'name'


class GameFactory:
    DEFAULT_PAGE_SIZE = 100
    DEFAULT_MAX_PAGES = 100
    REPLAY_URL = 'http://generals.io/api/replaysForUsername'

    def __init__(self, players, page_size=DEFAULT_PAGE_SIZE, max_pages=DEFAULT_MAX_PAGES):
        self._page_size = page_size
        self._max_pages = max_pages
        self._players = {username: player for player in players for username in player.usernames}
        self._games = None

    def get_games(self,
                  game_type=None,
                  time_sort=True,
                  filter_untracked_players=False,
                  strict_filter=True,
                  use_cache=True):
        # Get a unique list of games over all tracked players
        game_map = dict()
        for username in self._players:
            player_game_dicts = GameFactory._pull_replays(username, self._page_size,
                                                          self._max_pages, use_cache)
            for game_dict in player_game_dicts:
                game = self._create_game(game_dict)
                game_map[game.game_id] = game
        self._games = list(game_map.values())

        # Filter by game type
        if game_type is not None:
            self._games = [game for game in game_map.values() if game.game_type == game_type]

        # Filter out untracked players from game rankings
        if filter_untracked_players:
            player_names = set([player.name for _, player in self._players.items()])
            self._games = GameFactory._filter_untracked(self._games, player_names,
                                                        strict_filter=strict_filter)

        # Sort games by when they occurred
        if time_sort:
            self._games = sorted(self._games, key=lambda game: game.game_time)
        return self._games

    @classmethod
    def _filter_untracked(cls,
                          games,
                          player_names,
                          strict_filter=True):
        """
        Get a list of games where the rankings only include players from a given set.

        :param player_names: Players to keep in rankings.
        :param strict_filter: Filter out those games that contain non-tracked players.
        """
        tracked_games = []
        for game in games:
            n_players = len(game.ranking)
            n_game_tracked = len(player_names.intersection(game.ranking))

            # If strict, filter out all games that have any untracked players
            if strict_filter and n_game_tracked != n_players:
                continue

            # Filter out all games where only one player is tracked
            if n_game_tracked < 2:
                continue

            game.ranking = [player for player in game.ranking if player in player_names]
            tracked_games.append(game)
        return tracked_games

    @classmethod
    def _pull_replays(cls, username, page_size, max_pages, use_cache):
        username_hash = hashlib.sha1(username.encode('UTF-8')).hexdigest()
        cache_file = f'cache/user-games-{username_hash}.json'
        if use_cache and os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)

        game_dicts = []
        for page_number in range(max_pages):
            if page_number == max_pages - 1:
                print("WARNING: max pages reached when pulling game data")

            offset = page_size * page_number
            params = {'u': username, 'offset': offset, 'count': page_size}
            response = requests.get(url=GameFactory.REPLAY_URL, params=params)
            page_game_dicts = response.json()

            game_dicts.extend(page_game_dicts)
            if len(page_game_dicts) < page_size:
                break

        if not os.path.exists('cache'):
            os.makedirs('cache')
        with open(cache_file, 'w') as f:
            json.dump(game_dicts, f)
        return game_dicts

    def _create_game(self, game_dict):
        game_id = game_dict[_GameConstants._ID]
        game_type = game_dict[_GameConstants._TYPE]

        # Game start time is stored in unix time with millisecond precision
        game_time = datetime.fromtimestamp(game_dict[_GameConstants._START_TIME] / 1000)

        # Convert usernames to player names if they are registered
        # Discard number of stars a player has, no one cares
        ranking = []
        for ranking_record in game_dict[_GameConstants._RANKING]:
            username = ranking_record[_GameConstants._USERNAME]
            name = self._players[username].name if username in self._players else username
            ranking.append(name)

        # There are actually two steps per turn
        n_turns = game_dict[_GameConstants._TURNS] / 2

        return Game(game_id, game_type, game_time, ranking, n_turns)
