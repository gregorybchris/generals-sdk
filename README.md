# SDK for Accessing Generals Data

## Installation

```bash
git clone git@github.com:gregorybchris/generals-sdk.git
cd generals-sdk
pip install -e .
```

## Usage

```python
from generals_sdk.games.game import Game
from generals_sdk.games.game_factory import GameFactory
from generals_sdk.players.player import Player

players = [Player('<your-name>', ['<your-generals-username>'])]
factory = GameFactory(players, use_cache=True)
games = factory.get_games(game_type=Game.TYPE_CUSTOM)
for game in games:
    print(game)
```
