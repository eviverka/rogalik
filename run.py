import curses
import sys
import os
from game.gameloop import game_loop

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

if __name__ == "__main__":
    curses.wrapper(game_loop)