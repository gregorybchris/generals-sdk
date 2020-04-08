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
    DEFAULT_CACHE_DIR = './cache/games'
    REPLAY_URL = 'http://generals.io/api/replaysForUsername'

    def __init__(self,
                 players,
                 page_size=DEFAULT_PAGE_SIZE,
                 max_pages=DEFAULT_MAX_PAGES,
                 use_cache=True,
                 cache_dir=DEFAULT_CACHE_DIR):
        self._page_size = page_size
        self._max_pages = max_pages
        self._use_cache = use_cache
        self._cache_dir = cache_dir
        self._players = {username: player for player in players for username in player.usernames}
        self._games = None

    def get_games(self,
                  game_type=None,
                  time_sort=True,
                  all_in_game_players_tracked=False,
                  all_tracked_players_in_game=False,
                  filter_untracked=False):
        # Get a unique list of games over all tracked players
        game_map = dict()
        for username in self._players:
            player_game_dicts = GameFactory._pull_games(username,
                                                        self._page_size, self._max_pages,
                                                        self._use_cache, self._cache_dir)
            for game_dict in player_game_dicts:
                game = self._create_game(game_dict)
                game_map[game.game_id] = game
        self._games = list(game_map.values())

        # Filter by game type
        if game_type is not None:
            self._games = [game for game in game_map.values() if game.game_type == game_type]

        # Filter out untracked players from game rankings
        if all_in_game_players_tracked or all_tracked_players_in_game or filter_untracked:
            player_names = set([player.name for _, player in self._players.items()])
            self._games = GameFactory._filter(self._games, player_names,
                                              all_in_game_players_tracked,
                                              all_tracked_players_in_game,
                                              filter_untracked)

        # Sort games by when they occurred
        if time_sort:
            self._games = sorted(self._games, key=lambda game: game.game_time)
        return self._games

    @classmethod
    def _filter(cls,
                games,
                player_names,
                all_in_game_players_tracked,
                all_tracked_players_in_game,
                filter_untracked):
        """
        Get a list of games where the rankings only include players from a given set.

        :param player_names: Players to keep in rankings.
        :param all_in_game_players_tracked: Filter out games where not all players are tracked.
        :param all_tracked_players_in_game: Filter out games where not all tracked players are playing.
        :param filter_untracked: Filter out untracked players from rankings.
        """
        tracked_set = set(player_names)

        filtered_games = []
        for game in games:
            in_game_set = set(game.ranking)

            if all_tracked_players_in_game and len(tracked_set - in_game_set) != 0:
                continue

            if all_in_game_players_tracked and len(in_game_set - tracked_set) != 0:
                continue

            if filter_untracked:
                game.ranking = [name for name in game.ranking if name in tracked_set]
                if len(game.ranking) < 2:
                    continue

            filtered_games.append(game)
        return filtered_games

    @classmethod
    def _pull_games(cls, username, page_size, max_pages, use_cache, cache_dir):
        username_hash = hashlib.sha1(username.encode('UTF-8')).hexdigest()
        cache_file = os.path.join(cache_dir, f'user-games-{username_hash}.json')
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

        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
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

        # The website will show half this number
        n_turns = game_dict[_GameConstants._TURNS]

        return Game(game_id, game_type, game_time, ranking, n_turns)
