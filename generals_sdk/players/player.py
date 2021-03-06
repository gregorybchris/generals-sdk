class Player:
    __slots__ = 'name', 'usernames'

    def __init__(self, name, usernames):
        if not isinstance(usernames, list):
            raise ValueError("usernames must be a list")

        self.name = name
        self.usernames = usernames

    def __repr__(self):
        return f"Player[name={self.name}, usernames=[{self.usernames}]]"
