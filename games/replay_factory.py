import json
import os
import requests
import subprocess

from .replay import Replay


class _ReplayConstants:
    _VERSION = 'version'
    _WIDTH = 'mapWidth'
    _HEIGHT = 'mapHeight'
    _USERNAMES = 'usernames'
    _GENERALS = 'generals'
    _CITIES = 'cities'
    _CITY_ARMIES = 'cityArmies'
    _MOUNTAINS = 'mountains'

    _MOVES = 'moves'
    _INDEX = 'index'
    _START = 'start'
    _END = 'end'
    _IS_50 = 'is50'
    _TURN = 'turn'


class ReplayFactory:
    REPLAY_URL = 'https://generalsio-replays-na.s3.amazonaws.com'
    DEFAULT_CACHE_DIR = './cache/replays'

    def __init__(self, cache_dir=DEFAULT_CACHE_DIR):
        self._cache_dir = cache_dir

    def get_replay(self, game):
        ReplayFactory._pull_replay(game.game_id, self._cache_dir)
        replay_data = ReplayFactory._decode_replay(game.game_id, self._cache_dir)

        version = replay_data[_ReplayConstants._VERSION]
        width = replay_data[_ReplayConstants._WIDTH]
        height = replay_data[_ReplayConstants._HEIGHT]

        def convpos(p, w):
            return p // w, p % w

        # TODO: Convert these to something structured
        # Note that all board locations start at 1 at the top left corner
        usernames = replay_data[_ReplayConstants._USERNAMES]
        generals = [convpos(p, width) for p in replay_data[_ReplayConstants._GENERALS]]
        cities = replay_data[_ReplayConstants._CITIES]
        city_armies = replay_data[_ReplayConstants._CITY_ARMIES]
        mountains = replay_data[_ReplayConstants._MOUNTAINS]
        moves = replay_data[_ReplayConstants._MOVES]

        return Replay(version, width, height, usernames, generals, cities, city_armies, mountains, moves)

    @staticmethod
    def clean_stream(stream, encoding='UTF-8'):
        return stream.decode(encoding).strip()

    @staticmethod
    def run_command(command_tokens, cwd=None, encoding='UTF-8'):
        p = subprocess.Popen(command_tokens, cwd=cwd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        return ReplayFactory.clean_stream(out), ReplayFactory.clean_stream(err)

    @classmethod
    def _decode_replay(cls, game_id, cache_dir):
        # TODO: Update this path based on the Python path
        convert_script = 'conversion/convert-replay.js'
        in_file = os.path.join(cache_dir, f'{game_id}.gior')
        out, err = ReplayFactory.run_command(['node', convert_script, in_file])
        if len(err) > 0:
            raise OSError(err)

        out_file = os.path.join(cache_dir, f'{game_id}.gioreplay')
        with open(out_file, 'r') as f:
            return json.load(f)

    @classmethod
    def _pull_replay(cls, game_id, cache_dir):
        cache_file = os.path.join(cache_dir, f'{game_id}.gior')
        if os.path.exists(cache_file):
            return

        replay_url = f'{ReplayFactory.REPLAY_URL}/{game_id}.gior'
        response = requests.get(url=replay_url)

        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        with open(cache_file, 'wb') as f:
            f.write(response.content)
