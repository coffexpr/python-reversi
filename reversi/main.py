import json
import re
import sys
from pathlib import Path
from sys import stderr

from .reversi import ConsoleReversi


non_num = re.compile(r'\D+')
saved_file = Path('pyreversi.json')
default_settings = {
    'game': {
        'board': {'size_x': 8, 'size_y': 8},
        'players': [
            {'name': 'black', 'disc': {'name': 'black', 'symbol': '●'}},
            {'name': 'white', 'disc': {'name': 'white', 'symbol': '○'}}
        ]
    }
}


def main(reversi):
    try:
        reversi.start()
    except (KeyboardInterrupt, EOFError):
        stderr.write('\n')
        try:
            c = input(f'Save progress as {saved_file}? (y/n): ')
        except (KeyboardInterrupt, EOFError):
            return
        if c == 'y':
            with open(saved_file, 'w') as f:
                f.write(json.dumps(reversi.serialize()))


def command():
    import argparse

    parser = argparse.ArgumentParser(description='Play reversi')
    parser.add_argument('--size', metavar=('witdh', 'height'), type=int, nargs=2, default=(8, 8),
                        help='Size of the board')
    parser.add_argument('--players', nargs='+', default=('●', '○'),
                        help='Player discs')
    parser.add_argument('--hints', action='store_true')
    parser.add_argument('--setting-file')

    args = parser.parse_args()
    if args.setting_file is not None:
        with open(args.setting_file) as f:
            reversi = ConsoleReversi.deserialize(json.load(f))
    elif len(sys.argv) < 2 and saved_file.exists():
        with open(saved_file) as f:
            reversi = ConsoleReversi.deserialize(json.load(f))
    else:
        settings = dict(
            game=dict(
                board=dict(size_x=args.size[0], size_y=args.size[1]),
                players=[dict(name=f'player{i}', disc=dict(name='disc{i}', symbol=p))
                         for i, p in enumerate(args.players)]))
        reversi = ConsoleReversi.deserialize(settings)
        reversi.game.setup()
    main(reversi)
