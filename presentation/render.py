import curses

from domain.map import *
from domain.entities import *
from domain.game_session import *

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
        curses.init_pair(7, curses.COLOR_BLUE, 8)
        curses.init_pair(8, curses.COLOR_RED, 8)
        curses.init_pair(9, curses.COLOR_YELLOW, 8)
        curses.init_pair(10, curses.COLOR_BLUE, curses.COLOR_BLACK)
    
    def render_level(self, stdscr: curses.window, level: Level, player: Character, session: GameSession):
        stdscr.clear()
        self.render_room(stdscr, level)
        self.render_coridors_and_exits(stdscr, level)
        self.render_entities(stdscr, level, player)
        self.render_hud(stdscr, level, player, session, level.height+1)
        
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
                    if not is_inside_any_room and (x, y) not in level.doors:
                        stdscr.addch(y, x, ' ', curses.color_pair(4))

        if (level.exit_x, level.exit_y) in level.discovered_cells:
            stdscr.addch(level.exit_y, level.exit_x, '>', curses.color_pair(6))

        for (dx, dy), color in level.doors.items():
            if (dx, dy) in level.discovered_cells:
                if color == "red":
                    stdscr.addch(dy, dx, 'D', curses.color_pair(8))
                if color == "yellow":
                    stdscr.addch(dy, dx, 'D', curses.color_pair(9))
                if color == "blue":
                    stdscr.addch(dy, dx, 'D', curses.color_pair(7))
    
    def render_entities(self, stdscr: curses.window, level: Level, player: Character, R: int = 7):
        def draw_item(y: int, x: int, item_type: str, name: str = ""):
            match item_type:
                case "treasure":
                    stdscr.addch(y, x, '*', curses.color_pair(3))
                case "food":
                    stdscr.addch(y, x, '%', curses.color_pair(5))
                case "elixirs":
                    stdscr.addch(y, x, '!', curses.color_pair(5))
                case "scrolls":
                    stdscr.addch(y, x, '?', curses.color_pair(5))
                case "weapons":
                    stdscr.addch(y, x, ')', curses.color_pair(5))
                case "key":
                    if name == "red_key":
                        stdscr.addch(y, x, 'k', curses.color_pair(2))
                    if name == "yellow_key":
                        stdscr.addch(y, x, 'k', curses.color_pair(3))
                    if name == "blue_key":
                        stdscr.addch(y, x, 'k', curses.color_pair(10))

        for item in level.items:
            distance = abs(item.x - player.x) + abs(item.y - player.y)
            if (item.x, item.y) in level.discovered_cells and distance <= R:
                draw_item(item.y, item.x, item.item_type, item.name)


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
                    case "mimic":
                        if not enemy.is_disguised:
                            stdscr.addch(enemy.y, enemy.x, 'm', curses.color_pair(5))
                        else:
                            draw_item(enemy.y, enemy.x, enemy.is_disguised_as)
        stdscr.addch(player.y, player.x, '@')

    def render_hud(self, stdscr: curses.window, level: Level, player: Character, session: GameSession, line: int = 24, col: int = 0):
        if player.current_weapon is not None:
            weapon_name = f"{player.current_weapon.name}"
        else: 
            weapon_name = "Безоружен"

        keys_hud = ""
        if "red_key" in player.keys: keys_hud += "[R]"
        if "yellow_key" in player.keys: keys_hud += "[Y]"
        if "blue_key" in player.keys: keys_hud += "[B]"
        if not keys_hud: keys_hud = "Нет"

        hud_text = (
            f"Ярус: {level.index} | "
            f"HP: {player.health}/{player.max_health} | "
            f"STR: {player.strength} | "
            f"DEX: {player.dexterity} | "
            f"Оружие: {weapon_name} | "
            f"Золото: {player.gold} | "
            f"Ключи: {keys_hud}"
        )
        stdscr.addstr(line, col, hud_text)
        if getattr(session, "message", ""):
            stdscr.addstr(line + 1, col, session.message, curses.color_pair(2))
    
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
        
