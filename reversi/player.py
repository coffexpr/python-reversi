class Player:

    def __init__(self, name, disc):
        self.name = name
        self.disc = disc

    def __repr__(self):
        return f'<Player {self.name!r}, {self.disc.symbol!r}>'
