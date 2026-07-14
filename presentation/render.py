import curses

from domain.map import *
from domain.entities import *

class GameRenderer:
    def init_screen(self, stdscr: curses.window):
        curses.curs_set(0)
        curses.init_color(8, 195, 195, 195)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, 8, 8)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    
    def render_level(self, stdscr: curses.window, level: Level, player: Character):
        stdscr.clear()
        self.render_room(stdscr, level)
        self.render_coridors_and_exits(stdscr, level)
        self.render_entities(stdscr, level, player)
        self.render_hud(stdscr, level, player, level.height+1)
        

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
                    is_inside_any_room = any (room.has_point(x,y) for room in level.rooms)
                    if not is_inside_any_room:
                        stdscr.addch(y, x, ' ', curses.color_pair(4))
        if (level.exit_x, level.exit_y) in level.discovered_cells:
            stdscr.addch(level.exit_y, level.exit_x, '>', curses.color_pair(6))
    
    def render_entities(self, stdscr: curses.window, level: Level, player: Character, R: int = 7):

        for item in level.items:
            distance = abs(item.x - player.x) + abs(item.y - player.y)
            if (item.x, item.y) in level.discovered_cells and distance <= R:
                match item.item_type:
                    case "treasure":
                        stdscr.addch(item.y, item.x, '*', curses.color_pair(3))
                    case "food":
                        stdscr.addch(item.y, item.x, '%', curses.color_pair(5))
                    case "elixirs":
                        stdscr.addch(item.y, item.x, '!', curses.color_pair(5))
                    case "scrolls":
                        stdscr.addch(item.y, item.x, '?', curses.color_pair(5))
                    case "weapons":
                        stdscr.addch(item.y, item.x, ')', curses.color_pair(5))


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

    def render_hud(self, stdscr: curses.window, level: Level, player: Character, line: int = 24, col: int = 0):
        if player.current_weapon is not None:
            weapon_name = f"{player.current_weapon.name} (+{player.current_weapon.strength_bonus})"
        else: 
            weapon_name = "Безоружен"
        hud_text = (
            f"Ярус: {level.index} | "
            f"HP: {player.health}/{player.max_health} | "
            f"STR: {player.strength} | "
            f"DEX: {player.dexterity} | "
            f"Оружие: {weapon_name} | "
            f"Золото: {player.gold}"
        )
        stdscr.addstr(line, col, hud_text)
    
    def render_inventory(self, stdscr: curses.window, level: Level, player: Character, item_type: str, line: int = 15, col: int = 5) -> int:
        stdscr.clear()
        items: list[Item] = player.backpack[item_type]
        if len(items) > 0:
            stdscr.addstr(line, col, f"--- ВАШ РЮКЗАК ({item_type})")
            for i, item in enumerate(items):
                item_text = f"{i+1}. {item.name}"
                stdscr.addstr(line+i+2, col, item_text)
            stdscr.addstr(line+len(items)+2, col, "Выберите слот (1-9) или любую другую клавишу для отмены...")
        else:
            stdscr.addstr(line + 1, col, "Рюкзак пуст. Нажмите любую клавишу...")
            stdscr.refresh()
            stdscr.getch()
            return -1
        
        key = stdscr.getch()
        if 49 <= key <= 57:
            return key - 48
        
        return -1
        
