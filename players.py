class Player:
    __slots__ = 'name', 'usernames'

    def __init__(self, name, usernames):
        self.name = name
        self.usernames = usernames


class Players:
    CHRIS = Player('Chris', ['SpaceGeneral'])
    GIDEON = Player('Gideon', ['gwulfs'])
    JACK = Player('Jack', ['SoyJuan'])
    JANET = Player('Janet', ['OhWhale'])
    JASON = Player('Jason', ['Blooj'])
    JONATHAN = Player('Jonathan', ['graphpaper'])
    KEVIN = Player('Kevin', ['kevinlust', 'kevlust'])
    LEXI = Player('Lexi', ['gallexi', 'LexiG', 'Lexiiii'])
    LOGAN = Player('Logan', ['general280'])
    MAX = Player('Max', ['tekknolagi', 'noelle'])  # Also possibly 'General DUHT'
    MIKE = Player('Mike', ['Chitalian'])
    ROBERT = Player('Robert', ['Crhis', 'Cirhs'])
    RYAN = Player('Ryan', ['rosgoo', 'rosgood'])
    YUKI = Player('Yuki', ['yukismash', 'yukismash!'])
