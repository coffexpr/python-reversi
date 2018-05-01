from setuptools import setup

package = 'Python reversi'
version = '0.1'

setup(name=package,
      version=version,
      packages=['reversi'],
      description="Python reversi",
      entry_points={
          'console_scripts': [
              'reversi = reversi.main:command',
          ],
      },
      url='https://github.com/coffexpr/python-reversi')
