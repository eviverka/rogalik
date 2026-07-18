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

SAVE_DIRECTORY = "saves"
SAVE_FILE_MASK = "gamesave_.json"

ENEMY_BALANCING = {
    "zombie":     {"max_health": 30, "strength": 2, "dexterity": 2,  "hostility": 4},
    "vampire":    {"max_health": 25, "strength": 4, "dexterity": 8,  "hostility": 6},
    "ghost":      {"max_health": 10, "strength": 2, "dexterity": 7,  "hostility": 5},
    "ogre":       {"max_health": 45, "strength": 10,"dexterity": 3,  "hostility": 4},
    "snake_mage": {"max_health": 15, "strength": 3, "dexterity": 10, "hostility": 7},
    "mimic":      {"max_health": 40, "strength": 2, "dexterity": 12, "hostility": 2}
}
