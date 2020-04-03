# Generals Game Data Analysis

## Environment Setup

```bash
pip install -r requirements.txt
```

## Interface Usage

```python
factory = GameFactory(tracked_players)
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