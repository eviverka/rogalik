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

class Character(Creature):
    def __init__(self, start_x: int, start_y: int, max_health: int, strength: int, dexterity: int, current_weapon = None, backpack = None):
        super().__init__(start_x, start_y, max_health, strength, dexterity)
        self.gold = 0

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
                self.strength += item.strength_bonus
                self.dexterity += item.dexterity_bonus
                return True, None
            case "elixirs":
                self.max_health += item.max_health_bonus
                self.health += item.max_health_bonus
                self.strength += item.strength_bonus
                self.dexterity += item.dexterity_bonus
                return True, None
            case "weapons":
                old_weapon = self.current_weapon
                self.current_weapon = item
                return True, old_weapon
                

class Enemy(Creature):
    def __init__(self, start_x: int, start_y: int, enemy_type: str):
        super().__init__(start_x, start_y)

        self.enemy_type = enemy_type

        match enemy_type:
            case "zombie":
                self.max_health = 30
                self.strength = 5
                self.dexterity = 2
                self.hostility = 3
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
                self.hostility = 2
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
