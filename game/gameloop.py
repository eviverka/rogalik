from domain.entities import *
from domain.map import *
from domain.game_session import *
from presentation.render import *
from data.save_manager import *
from data.scoreboard import *
from config import *

def initialize_session(player_name: str, level_generator: LevelGenerator, save_manager: SaveManager) -> GameSession:
    save_data = save_manager.load_game()

    if not save_data == None:
        session = GameSession.from_dict(save_data, level_generator)
    else:
        first_level, start_x, start_y = level_generator.build_level(1)
        player = Character(start_x, start_y, INITIAL_PLAYER_HP, INITIAL_PLAYER_STR, INITIAL_PLAYER_DEX)
        session = GameSession(player, first_level, level_generator)

    return session

def handle_inventory_interaction(renderer: GameRenderer, session: GameSession, stdscr: curses.window, item_type: str):
    item_key = renderer.render_inventory(stdscr, session.current_level, session.player, item_type)
    if not item_key == -1:
        session.use_backpack_item(item_type, item_key)

def get_player_name(stdscr: curses.window) -> str:
    curses.echo()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(height//2, width//2-30, "Введите имя вашего персонажа: ", curses.A_BOLD)
    stdscr.refresh()
    player_name = stdscr.getstr().decode('utf-8', errors='ignore').strip()
    if not player_name:
        player_name = "Hero"
    curses.noecho()
    return player_name

def finalize_game(player_name: str, session: GameSession, save_manager: SaveManager):
    if session.is_game_over:
        save_manager.delete_save()
    scoreboard = ScoreboardManager()
    scoreboard.add_score(player_name, session)


def game_loop(stdscr: curses.window):
    renderer = GameRenderer()
    player_name = get_player_name(stdscr)
    level_generator = LevelGenerator(MAP_WIDTH, MAP_HEIGHT)
    save_manager = SaveManager(f"{SAVE_DIRECTORY}/{player_name}/{SAVE_FILE_MASK}")
    session = initialize_session(player_name, level_generator, save_manager)
    renderer.init_screen(stdscr)
    while not session.is_game_over and not session.is_victory:
        renderer.render_level(stdscr, session.current_level, session.player, session)
        stdscr.refresh()
        key_code = stdscr.getch()
        key = chr(key_code) if 0 <= key_code <= 255 else ""
        match key:
            case 'w': session.try_move_player(0, -1)
            case 'a': session.try_move_player(-1,0)
            case 's': session.try_move_player(0,1)
            case 'd': session.try_move_player(1,0)
            case 'h': handle_inventory_interaction(renderer, session, stdscr, "food")
            case 'e': handle_inventory_interaction(renderer, session, stdscr, "elixirs")
            case 'k': handle_inventory_interaction(renderer, session, stdscr, "scrolls")
            case 'j': handle_inventory_interaction(renderer, session, stdscr, "weapons")
            case 'q':
                save_manager.save_game(session.to_dict())
                break
    finalize_game(player_name, session, save_manager)