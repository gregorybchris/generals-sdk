class Replay:
    def __init__(self,
                 version,
                 width,
                 height,
                 usernames,
                 generals,
                 cities,
                 city_armies,
                 mountains,
                 moves):
        self.version = version
        self.width = width
        self.height = height
        self.usernames = usernames
        self.generals = generals
        self.cities = cities
        self.city_armies = city_armies
        self.mountains = mountains
        self.moves = moves
