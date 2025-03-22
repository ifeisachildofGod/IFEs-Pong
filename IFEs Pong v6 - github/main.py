# import pyuac
# import pywintypes
# from .game.Game import GameApp
# from .game.game_constants import SCR_SIZE
from src.game import Game
# import sys
# import os

# @pyuac.main_requires_admin
def main():
    game = Game((1200, 600))
    game.loop()

if __name__ == '__main__':
    # try:
    main()
    # except (pywintypes.error, PermissionError):
    #     sys.exit()
    # except AttributeError:
    #     stdout_temp_fn = 'pyuac.stdout.tmp.txt'
    #     stderr_temp_fn = 'pyuac.stderr.tmp.txt'
    #     if os.path.exists(stdout_temp_fn):
    #         os.remove(stdout_temp_fn)
    #     if os.path.exists(stderr_temp_fn):
    #         os.remove(stderr_temp_fn)


