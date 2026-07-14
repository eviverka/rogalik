from domain.entities import *
from domain.map import *
from domain.game_session import *
from presentation.render import *
from data.save_manager import *
from data.scoreboard import *

def game_loop(stdscr: curses.window):
    curses.echo()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(height//2, width//2-30, "Введите имя вашего персонажа: ", curses.A_BOLD)
    stdscr.refresh()
    player_name = stdscr.getstr().decode('utf-8', errors='ignore').strip()
    if not player_name:
        player_name = "Hero"
    curses.noecho()
    renderer = GameRenderer()
    level_generator = LevelGenerator(102, 34)
    save_manager = SaveManager(f"saves/{player_name}/gamesave_.json")
    save_data = save_manager.load_game()
    if not save_data == None:
        session = GameSession.from_dict(save_data, level_generator)
    else:
        first_level, start_x, start_y = level_generator.build_level(1)
        player = Character(start_x, start_y, 20, 6, 5)
        session = GameSession(player, first_level, level_generator)
    renderer.init_screen(stdscr)
    while not session.is_game_over and not session.is_victory:
        renderer.render_level(stdscr, session.current_level, session.player)
        stdscr.refresh()
        key_code = stdscr.getch()
        key = chr(key_code) if 0 <= key_code <= 255 else ""
        match key:
            case 'w':
                session.try_move_player(0, -1)
            case 'a':
                session.try_move_player(-1,0)
            case 's':
                session.try_move_player(0,1)
            case 'd':
                session.try_move_player(1,0)
            case 'h':
                item_key = renderer.render_inventory(stdscr, session.current_level, session.player, "food")
                if not item_key == -1:
                    session.use_backpack_item("food", item_key)
            case 'e':
                item_key = renderer.render_inventory(stdscr, session.current_level, session.player, "elixirs")
                if not item_key == -1:
                    session.use_backpack_item("elixirs", item_key)
            case 'k':
                item_key = renderer.render_inventory(stdscr, session.current_level, session.player, "scrolls")
                if not item_key == -1:
                    session.use_backpack_item("scrolls", item_key)
            case 'j':
                item_key = renderer.render_inventory(stdscr, session.current_level, session.player, "weapons")
                if not item_key == -1:
                    session.use_backpack_item("weapons", item_key)
            case 'q':
                save_manager.save_game(session.to_dict())
                break
    scoreboard = ScoreboardManager()
    scoreboard.add_score(player_name, session)
            