from collections import Counter

from .formatter import ConsoleFormatter


class GameIsEnd(Exception):
    pass


class Game:

    def __init__(self, board, players, player_index=0):
        self.board = board
        self.players = players
        self.player_index = player_index
        self.puttables = set()
        self._disc_map = {int(p.disc): p.disc for p in self.players}
        self._disc_map[int(self.board.EMPTY)] = self.board.EMPTY
        self._update_puttables()
        self._formatter = ConsoleFormatter()

    def __repr__(self):
        return self._formatter(self)

    @property
    def player(self):
        return self.players[self.player_index]

    def get_disc(self, code):
        return self._disc_map.get(code)

    def _next_player(self, index=None):
        lp = len(self.players)
        idx = self.player_index if index is None else index
        idx = idx + 1
        if idx < lp:
            return idx
        else:
            return 0

    def _player_cycle(self, offset=0, limit=None):
        limit = len(self.players) if limit is None else int(limit)
        limit += offset
        idx = self.player_index
        for i, idx in enumerate(self._player_cycle_forever()):
            if i >= limit:
                break
            if i >= offset:
                yield idx

    def _player_cycle_forever(self):
        idx = self.player_index
        while True:
            yield idx
            idx = self._next_player(idx)

    def _update_puttables(self, disc=None):
        disc = self.player.disc if disc is None else disc
        self.puttables = self.board.puttables(disc)

    def setup(self):
        lp = len(self.players)
        x_begin = self.board.size_x // 2 - lp // 2
        y_begin = self.board.size_y // 2 - lp // 2
        if not (x_begin > 0 and y_begin):
            raise ValueError('Not enough board size')
        pc = self._player_cycle_forever()
        for dx in range(lp):
            for dy in range(lp):
                i = next(pc)
                disc = self.players[i].disc
                self.board[(x_begin + dx, y_begin + dy)] = int(disc)
            next(pc)
        self._update_puttables()
        return self

    def next_state(self):
        if self.puttables:
            return self
        for i in self._player_cycle(offset=1):
            self._update_puttables(self.players[i].disc)
            if self.puttables:
                self.player_index = i
                return self
        raise GameIsEnd('Game is end')

    def put(self, cell):
        if cell not in self.puttables:
            raise ValueError(f'Could not put: {cell!r}')
        disc = self.player.disc
        for c in self.board.flips(disc, cell) | {cell}:
            self.board[c] = disc
        self.puttables.clear()
        return self

    def count(self):
        return Counter(self.board)
