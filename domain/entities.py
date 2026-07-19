import random
from config import *

class Creature:
    def __init__(self, start_x: int = 0, start_y: int = 0, max_health: int = 10, strength: int = 5, dexterity: int = 5, name: str = ""):
        if max_health<=0:
            max_health = 10

        self.x = start_x
        self.y = start_y
        self.max_health = max_health
        self.health = max_health
        self.strength = strength
        self.dexterity = dexterity
        self.name = name

class Item:
    def __init__(self, x: int, y: int, item_type: str, name: str, health_bonus = 0, max_health_bonus = 0, strength_bonus = 0, dexterity_bonus = 0, cost = 0):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.name = name
        self.health_bonus = health_bonus
        self.max_health_bonus = max_health_bonus
        self.strength_bonus = strength_bonus
        self.dexterity_bonus = dexterity_bonus
        self.cost = cost

    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "item_type": self.item_type,
            "name": self.name,
            "health_bonus": self.health_bonus,
            "max_health_bonus": self.max_health_bonus,
            "strength_bonus": self.strength_bonus,
            "dexterity_bonus": self.dexterity_bonus,
            "cost": self.cost
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            x=data["x"],
            y=data["y"],
            item_type=data["item_type"],
            name=data["name"],
            health_bonus=data["health_bonus"],
            max_health_bonus=data["max_health_bonus"],
            strength_bonus=data["strength_bonus"],
            dexterity_bonus=data["dexterity_bonus"],
            cost=data["cost"]
        )

class Character(Creature):
    def __init__(self, start_x: int, start_y: int, max_health: int, strength: int, dexterity: int, current_weapon: Item = None, backpack = None, name: str = ""):
        super().__init__(start_x, start_y, max_health, strength, dexterity, name)
        self.gold = 0
        self.keys = set()

        self.current_weapon = current_weapon
        if backpack is None:
            self.backpack = {
                "food": [],
                "elixirs": [],
                "scrolls": [],
                "weapons": []
            }
        else:
            self.backpack = backpack
    
    def pick_up_item(self, item: Item) -> bool:
        category = item.item_type
        if category == "treasure":
            self.gold += item.cost
            return True
        elif item.item_type == "key":
            self.keys.add(item.name)
            return True
        elif len(self.backpack[category]) < MAX_BACKPACK_SLOT_CAPACITY:
            self.backpack[category].append(item)
            return True
        else:
            return False
    
    def use_item_by_index(self, item_type: str, index: int) -> tuple[bool, Item]:
        index -= 1
        if 0 <= index < len(self.backpack[item_type]):
            item: Item = self.backpack[item_type].pop(index)
        else:
            return False, None
        
        match item_type:
            case "food":
                self.health = min(self.health + item.health_bonus, self.max_health)
                return True, None
            case "scrolls":
                self.max_health += item.max_health_bonus
                self.health += item.max_health_bonus
                self.health += item.health_bonus
                self.health = min(self.max_health, self.health)
                self.strength += item.strength_bonus
                self.dexterity += item.dexterity_bonus
                return True, None
            case "elixirs":
                self.max_health += item.max_health_bonus
                self.health += item.max_health_bonus
                self.health += item.health_bonus
                self.health = min(self.max_health, self.health)
                self.strength += item.strength_bonus
                self.dexterity += item.dexterity_bonus
                return True, None
            case "weapons":
                old_weapon = self.current_weapon
                self.current_weapon = item
                return True, old_weapon
    
    def to_dict(self) -> dict:
        backpack_dict = {
            "food": [item.to_dict() for item in self.backpack["food"]],
            "elixirs": [item.to_dict() for item in self.backpack["elixirs"]],
            "scrolls": [item.to_dict() for item in self.backpack["scrolls"]],
            "weapons": [item.to_dict() for item in self.backpack["weapons"]]
        }
        return {
            "x": self.x,
            "y": self.y,
            "health": self.health,
            "max_health": self.max_health,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "gold": self.gold,
            "current_weapon": self.current_weapon.to_dict() if self.current_weapon else None,
            "backpack": backpack_dict,
            "keys": list(self.keys)
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        player = cls(
            start_x = data["x"],
            start_y = data["y"],
            max_health=data["max_health"],
            strength=data["strength"],
            dexterity=data["dexterity"]
        )
        
        player.health = data["health"]
        player.gold = data["gold"]
        player.keys = set(data["keys"])

        if data["current_weapon"] is not None:
            player.current_weapon = Item.from_dict(data["current_weapon"])
        else:
            player.current_weapon = None

        player.backpack = {
            "food": [Item.from_dict(item_data) for item_data in data["backpack"]["food"]],
            "elixirs": [Item.from_dict(item_data) for item_data in data["backpack"]["elixirs"]],
            "scrolls": [Item.from_dict(item_data) for item_data in data["backpack"]["scrolls"]],
            "weapons": [Item.from_dict(item_data) for item_data in data["backpack"]["weapons"]]
        }
        
        return player
                
class Enemy(Creature):
    def __init__(self, start_x: int, start_y: int, enemy_type: str, name: str):
        super().__init__(start_x, start_y, name=name)
        self.enemy_type = enemy_type
        
        stats = ENEMY_DATABASE.get(enemy_type, {"max_health": 10, "strength": 2, "dexterity": 2, "hostility": 1})
        
        self.max_health = stats["max_health"]
        self.strength = stats["strength"]
        self.dexterity = stats["dexterity"]
        self.hostility = stats["hostility"]
        
        if enemy_type == "vampire":
            self.is_first_hit = True
        elif enemy_type == "ghost":
            self.is_invisible = False
        elif enemy_type == "ogre":
            self.is_resting = False
        elif enemy_type == "mimic":
            self.is_disguised = True
            available_items = list(ITEMS_DATABASE.keys())
            if "keys" in available_items:
                available_items.remove("keys")
            self.is_disguised_as = random.choice(available_items)
            
        self.health = self.max_health
    
    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "enemy_type": self.enemy_type,
            "health": self.health,
            "max_health": self.max_health,
            "is_first_hit": getattr(self, "is_first_hit", False),
            "is_resting": getattr(self, "is_resting", False),
            "is_disguised": getattr(self, "is_disguised", False),
            "is_disguised_as": getattr(self, "is_disguised_as", ""),
            "is_invisible": getattr(self, "is_invisible", False),
            "name": self.name
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        enemy = cls(data["x"], data["y"], data["enemy_type"], data["name"])
        enemy.health = data["health"]
        enemy.max_health = data["max_health"]

        if "is_first_hit" in data: enemy.is_first_hit = data["is_first_hit"]
        if "is_resting" in data: enemy.is_resting = data["is_resting"]
        if "is_invisible" in data: enemy.is_invisible = data["is_invisible"]
        
        if "is_disguised" in data: enemy.is_disguised = data["is_disguised"]
        if "is_disguised_as" in data: enemy.is_disguised_as = data["is_disguised_as"]
        
        return enemy
    