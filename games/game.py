class Game:
    __slots__ = 'game_id', 'game_type', 'game_time', 'ranking', 'n_turns'

    TYPE_1v1 = '1v1'
    TYPE_2v2 = '2v2'
    TYPE_CLASSIC = 'classic'  # AKA "FFA" 8 player free for all
    TYPE_CUSTOM = 'custom'  # Custom game with a room link

    def __init__(self, game_id, game_type, game_time, ranking, n_turns):
        self.game_id = game_id
        self.game_type = game_type
        self.game_time = game_time
        self.ranking = ranking
        self.n_turns = n_turns

    def __repr__(self):
        return (f"Game[id={self.game_id}, datetime={self.game_time}, type={self.game_type}, "
                f"ranking={self.ranking}, turns={self.n_turns}]")
