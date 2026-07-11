import curses

from domain.map import *
from domain.entities import *

class GameRenderer:
    def init_screen(self, stdscr: curses.window):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    def render_level(self, stdscr: curses.window, level: Level, player: Character):
        stdscr.clear()
        self.render_room(stdscr, level)
        self.render_coridors_and_exits(stdscr, level)
        self.render_entities(stdscr, level, player)
        

    def render_room(self, stdscr: curses.window, level: Level):
        for room in level.rooms:
            for y in range(room.y + 1, room.y + room.height - 1, 1):
                for x in range(room.x + 1, room.x + room.width - 1, 1):
                    if (x,y) in level.discovered_cells:
                        stdscr.addch(y, x, '.')

            for x in range(room.x, room.x + room.width):
                if (x, room.y) in level.discovered_cells:
                    stdscr.addch(room.y, x, '#')
                if (x, room.y + room.height - 1) in level.discovered_cells:    
                    stdscr.addch(room.y + room.height - 1, x, '#')
            
            for y in range(room.y, room.y + room.height):
                if (room.x, y) in level.discovered_cells:
                    stdscr.addch(y, room.x, '#')
                if (room.x + room.width - 1, y) in level.discovered_cells:
                    stdscr.addch(y, room.x + room.width - 1, '#')
    
    def render_coridors_and_exits(self, stdscr: curses.window, level: Level):
        for corridor in level.corridors:
            for x, y in corridor.points:
                if (x,y) in level.discovered_cells:
                    stdscr.addch(y, x, ' ', curses.color_pair(4))
        if (level.exit_x, level.exit_y) in level.discovered_cells:
            stdscr.addch(level.exit_y, level.exit_x, '>')
    
    def render_entities(self, stdscr: curses.window, level: Level, player: Character, R: int = 7):
        for enemy in level.enemies:
            distance = abs(enemy.x - player.x) + abs(enemy.y - player.y)
            if (enemy.x, enemy.y) in level.discovered_cells and distance <= R:
                match enemy.enemy_type:
                    case "zombie":
                        stdscr.addch(enemy.y, enemy.x, 'z', curses.color_pair(1))
                    case "vampire":
                        stdscr.addch(enemy.y, enemy.x, 'v', curses.color_pair(2))
                    case "ogre":
                        stdscr.addch(enemy.y, enemy.x, 'O', curses.color_pair(3))
                    case "snake_mage":
                        stdscr.addch(enemy.y, enemy.x, 's', curses.color_pair(5))
                    case "ghost":
                        if not enemy.is_invisible:
                            stdscr.addch(enemy.y, enemy.x, 'g', curses.color_pair(5))
        stdscr.addch(player.y, player.x, '@')