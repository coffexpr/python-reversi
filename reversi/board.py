import itertools

from .disc import Disc


class Board:
    EMPTY = Disc('empty', '  ')

    def __init__(self, size_x, size_y, board=None):
        self.size_x = int(size_x)
        self.size_y = int(size_y)
        if board is None:
            self.clear()
        else:
            self.board = board
            for c in self._cells_all():
                value = self[c]
                try:
                    int(value)
                except ValueError:
                    ValueError(f'Board contains invalid value: {c!r} -> {value!r}')

    def __repr__(self):
        return f'Board<{self.size_x!r}, {self.size_y!r}>'

    def __getitem__(self, cell):
        x, y = self._c2xy(cell)
        if x < 0 or y < 0:
            raise IndexError('Index must be > 0: (x, y) == {cell!r}')
        return self.board[y][x]

    def __setitem__(self, cell, value):
        x, y = self._c2xy(cell)
        code = int(value)
        if code == int(self.EMPTY):
            raise ValueError('Value must not be empty')
        self.board[y][x] = code

    def __iter__(self):
        for c in self._cells_all():
            yield self[c]

    def clear(self):
        self.board = [[int(self.EMPTY)
                       for x in range(self.size_x)]
                      for y in range(self.size_y)]

    def flips(self, disc, cell):
        return set(self._cells_flip_all_flattened(disc, cell))

    def puttables(self, disc):
        return set(self._cells_puttable(disc))

    def _c2xy(self, cells):
        x, y = cells
        return int(x), int(y)

    def _cells_all(self):
        for x in range(self.size_x):
            for y in range(self.size_y):
                yield x, y

    def _cells_code(self, code):
        for x, y in self._cells_all():
            if self[(x, y)] == code:
                yield x, y

    def _cells_empty(self):
        return self._cells_code(int(self.EMPTY))

    def _cells_toward(self, start_cell, delta):
        if delta == (0, 0):
            return
        x, y = self._c2xy(start_cell)
        dx, dy = self._c2xy(delta)
        try:
            while True:
                self[(x, y)]
                yield x, y
                x += dx
                y += dy
        except IndexError:
            return

    def _cells_flip(self, disc, cells):
        flips = set()
        for i, c in enumerate(cells):
            if i <= 0:
                continue
            code = self[c]
            if code == int(self.EMPTY):
                break
            if code == int(disc):
                return flips
            else:
                flips.add(c)
        return set()

    def _cells_flip_all(self, disc, cell):
        d = {-1, 0, 1}
        deltas = itertools.product(d, d)
        for d in deltas:
            yield self._cells_flip(disc, self._cells_toward(cell, d))

    def _cells_flip_all_flattened(self, disc, cell):
        return itertools.chain.from_iterable(self._cells_flip_all(disc, cell))

    def _puttable(self, disc, cell):
        if self[cell] == int(self.EMPTY):
            return bool(tuple(self._cells_flip_all_flattened(disc, cell)))
        else:
            return False

    def _cells_puttable(self, disc):
        for c in self._cells_empty():
            if self._puttable(disc, c):
                yield c
