class Creature:
    def __init__(self, start_x: int = 0, start_y: int = 0, max_health: int = 10, strength: int = 5, dexterity: int = 5):
        if max_health<=0:
            max_health = 10

        self.x = start_x
        self.y = start_y
        self.max_health = max_health
        self.health = max_health
        self.strength = strength
        self.dexterity = dexterity

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
    def __init__(self, start_x: int, start_y: int, max_health: int, strength: int, dexterity: int, current_weapon: Item = None, backpack = None):
        super().__init__(start_x, start_y, max_health, strength, dexterity)
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
        elif len(self.backpack[category]) < 9:
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
                if self.health > self.max_health:
                    self.health = self.max_health
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
    def __init__(self, start_x: int, start_y: int, enemy_type: str):
        super().__init__(start_x, start_y)

        self.enemy_type = enemy_type

        match enemy_type:
            case "zombie":
                self.max_health = 30
                self.strength = 3
                self.dexterity = 2
                self.hostility = 4
            case "vampire":
                self.max_health = 25
                self.strength = 4
                self.dexterity = 8
                self.hostility = 6
                self.is_first_hit: bool =  True
            case "ghost":
                self.max_health = 10
                self.strength = 2
                self.dexterity = 7
                self.hostility = 5
                self.is_invisible = False
            case "ogre":
                self.max_health = 45
                self.strength = 10
                self.dexterity = 3
                self.hostility = 4
                self.is_resting: bool = False
            case "snake_mage":
                self.max_health = 15
                self.strength = 3
                self.dexterity = 10
                self.hostility = 7
            case _:
                self.hostility = 1

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
            "is_invisible": getattr(self, "is_invisible", False)
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        enemy = cls(data["x"], data["y"], data["enemy_type"])
        enemy.health = data["health"]
        enemy.max_health = data["max_health"]
        setattr(enemy, "is_first_hit", data["is_first_hit"])
        setattr(enemy, "is_resting", data["is_resting"])
        setattr(enemy, "is_invisible", data["is_invisible"])
        return enemy