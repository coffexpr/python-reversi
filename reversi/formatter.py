class ConsoleFormatter:
    _hint_symbol = '・'

    def __init__(self, hint_symbol=None, hints_enabled=True):
        self.hint_symbol = type(self)._hint_symbol if hint_symbol is None else hint_symbol
        self.hints_enabled = hints_enabled

    def format(self, game):
        return self._player(game) + self._count(game) + '\n' + self._board(game)

    def _player(self, game):
        return f'Player: {game.player.disc.symbol}\n'

    def _count(self, game):
        s = 'Counts: '
        for i, count in game.count().items():
            disc = game.get_disc(i)
            if disc is not game.board.EMPTY:
                s += f'{disc.symbol}{count} '
        s += '\n'
        return s

    def _board(self, game):
        s = '  ' + ''.join([f'{i:2}' for i in range(game.board.size_x)]) + '\n'
        for y in range(game.board.size_y):
            s += f'{y:2}'
            for x in range(game.board.size_x):
                if self.hints_enabled and (x, y) in game.puttables:
                    s += self.hint_symbol
                else:
                    code = game.board[(x, y)]
                    s += game.get_disc(code).symbol
            s += '\n'
        return s

    def __call__(self, game):
        return self.format(game)
