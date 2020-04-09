# Generals Game Data Analysis

## Environment Setup

```bash
pip install -r requirements.txt
```

## Interface Usage

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
