import os
import re
import time
from sys import stderr, stdout

from .board import Board
from .disc import Disc
from .formatter import ConsoleFormatter
from .game import Game, GameIsEnd
from .player import Player


non_num = re.compile(r'\D+')


def get_cell_stdin(prompt=None):
    return extract_cell(input(prompt))


def extract_cell(s):
    x, y = [int(i) for i in non_num.split(s.strip())][:2]
    return x, y


class Reversi:

    def __init__(self, game):
        self.game = game

    def start(self):
        raise NotImplementedError()

    def serialize(self):
        return dict(
            game=dict(
                board=vars(self.game.board),
                players=[dict(name=i.name, disc=vars(i.disc))
                         for i in self.game.players],
                player_index=self.game.player_index))

    @classmethod
    def deserialize(cls, config):
        c = config['game']
        players = []
        for p in c['players']:
            d = p['disc']
            players.append(Player(p['name'], Disc(**d)))
        board = Board(**c['board'])
        return cls(Game(board, players, c.get('player_index', 0)))


class ConsoleReversi(Reversi):

    def __init__(self, game, formatter):
        super().__init__(game)
        self.formatter = formatter

    def show(self):
        stdout.write(self.formatter.format(self.game))

    def start(self):
        while True:
            os.system('clear')
            try:
                self.game.next_state()
            except GameIsEnd:
                break
            self.show()
            stdout.write('\n')
            try:
                self.game.put(get_cell_stdin('Put onto -> '))
            except ValueError as e:
                stderr.write(str(e))
                time.sleep(.2)
                stderr.write('Try again')
                time.sleep(1)
        self.show()

    def serialize(self):
        config = super().serialize()
        config['formatter'] = vars(self.formatter)
        return config

    @classmethod
    def deserialize(cls, config):
        game = Reversi.deserialize(config).game
        formatter = ConsoleFormatter(**config.get('formatter', {}))
        return cls(game, formatter)
