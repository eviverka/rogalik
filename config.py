MAP_WIDTH = 102
MAP_HEIGHT = 34

SECTOR_ROWS = 3
SECTOR_COLS = 3
TOTAL_SECTORS = SECTOR_ROWS * SECTOR_COLS

INITIAL_PLAYER_HP = 20
INITIAL_PLAYER_STR = 6
INITIAL_PLAYER_DEX = 5
PLAYER_VIEW_RADIUS = 7
MAX_BACKPACK_SLOT_CAPACITY = 9

BASE_HIT_CHANCE = 70
DEXTERITY_WEIGHT = 2
MIN_HIT_CHANCE = 3
MAX_HIT_CHANCE = 98

DDA_LOW_HEALTH_THRESHOLD = 0.3
DDA_STRESS_TURNS_LIMIT = 15 
DDA_STRESS_TURNS_EASY = 3      
DDA_EASY_MODIFIER = 0.7
DDA_HARD_MODIFIER = 1.3
DDA_MODIFIER_HARDNESS = 0.15
DDA_MODIFIER_HARDNESS_COEFF = 1.13
DDA_ENEMY_MAX_STR = 50

SAVE_DIRECTORY = "saves"
SAVE_FILE_MASK = "gamesave_.json"
SCOREBOARD_FILE_PATH = "scores/scoreboard.json"

ENEMY_DATABASE = {
    "zombie":     {"max_health": 30, "strength": 2, "dexterity": 2,  "hostility": 4},
    "vampire":    {"max_health": 25, "strength": 4, "dexterity": 8,  "hostility": 6},
    "ghost":      {"max_health": 10, "strength": 2, "dexterity": 7,  "hostility": 5},
    "ogre":       {"max_health": 45, "strength": 10,"dexterity": 3,  "hostility": 4},
    "snake_mage": {"max_health": 15, "strength": 3, "dexterity": 10, "hostility": 7},
    "mimic":      {"max_health": 40, "strength": 2, "dexterity": 12, "hostility": 2}
}

ITEMS_DATABASE = {
    "food": [
        {"name": "Спелое Яблоко (лечение: +4)", "health_bonus": 4},
        {"name": "Краюха Хлеба (лечение +6)", "health_bonus": 6},
        {"name": "Армейский Рацион (лечение +10)", "health_bonus": 10}
    ],
    "elixirs": [
        {"name": "Малое Зелье Лечения (лечение +8)", "health_bonus": 8},
        {"name": "Эликсир Огра (сила +2, макс. здоровье +2, лечение +5)", "strength_bonus": 2, "max_health_bonus": 5, "health_bonus": 5},
        {"name": "Зелье Кошачьей Грации (ловкость +3)", "dexterity_bonus": 3}
    ],
    "scrolls": [
        {"name": "Свиток Мудрости (макс. здоровье +3, лечение +3)", "max_health_bonus": 3, "health_bonus": 3},
        {"name": "Свиток Заточки Оружия (сила +1)", "strength_bonus": 1},
        {"name": "Древний Манускрипт (сила +2, ловкость +2)", "strength_bonus": 2, "dexterity_bonus": 2}
    ],
    "weapons": [
        {"name": "Ржавый Кинжал (+1)", "strength_bonus": 1},
        {"name": "Железный Короткий Меч (+3)", "strength_bonus": 3},
        {"name": "Стальной Двуручник (+5)", "strength_bonus": 5}
    ],
    "keys": [
        {"name": "red_key"},
        {"name": "yellow_key"},
        {"name": "blue_key"},
    ]
}