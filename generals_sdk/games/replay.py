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
                 moves,
                 teams,
                 map_title,
                 afks):
        self.version = version
        self.width = width
        self.height = height
        self.usernames = usernames
        self.generals = generals
        self.cities = cities
        self.city_armies = city_armies
        self.mountains = mountains
        self.moves = moves
        self.teams = teams
        self.map_title = map_title
        self.afks = afks

    def __repr__(self):
        return (f"Replay[version={self.version}, usernames={self.usernames}, teams={self.teams}]")
