# Generals Game Data Analysis

## Environment Setup

```bash
pip install -r requirements.txt
```

## Interface Usage

```python
from games.game import Game
from games.game_factory import GameFactory
from players import Player

players = [Player('<your-name>', '<your-generals-username>')]
factory = GameFactory(players)
games = factory.get_games(game_type=Game.TYPE_CUSTOM, use_cache=True)
for game in games:
    print(game)
```

## Running Altair Visualizations

```bash
jupyter nbextension install vega --py --sys-prefix
jupyter nbextension enable vega --py --sys-prefix
jupyter notebook
```