import random

from entities import *
from map import *

class GameSession:
    def __init__(self, player: Character, current_level: Level):
        self.player = player
        self.current_level = current_level
        self.steps_passed: int = 0
        self.enemies_killed: int = 0
        self.food_eaten: int = 0
        self.is_game_over = False

    def try_move_player(self, dx: int = 0, dy: int = 0):
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        if not self.current_level.is_walkable(new_x, new_y):
            return
        
        enemy_found = False
        for enemy in self.current_level.enemies:
            if enemy.x == new_x and enemy.y == new_y:
                enemy_found = True
                break
        
        if enemy_found:
            self.process_combat(self.player, enemy)
            self._update_enemies_turn()
            return
        
        self.player.x = new_x
        self.player.y = new_y
        self.steps_passed += 1
        for item in self.current_level.items:
            if item.x == self.player.x and item.y == self.player.y:
                success = self.player.pick_up_item(item)
                if success:
                    self.current_level.items.remove(item)
                    break
        self._update_enemies_turn()

    def process_combat(self, attacker: Creature, defender: Creature):
        damage = attacker.strength

        if isinstance(defender, Enemy):
            if defender.enemy_type == "vampire" and defender.is_first_hit:
                defender.is_first_hit = False
                return

        hit_chance = 70 + (attacker.dexterity * 2) - (defender.dexterity * 2)
        hit_chance = max(3, min(98, hit_chance))
        if random.randint(1, 100) > hit_chance:
            return

        if isinstance(attacker, Character) and attacker.current_weapon is not None:
            damage += attacker.current_weapon.strength_bonus

        defender.health -= damage

        if isinstance(attacker, Enemy):
            if attacker.enemy_type == "vampire":
                if self.player.max_health >= 3:
                    self.player.max_health -= 2
                else:
                    self.player.max_health = 1
            if attacker.enemy_type == "ogre":
                attacker.is_resting = True

        if defender.health <= 0:
            if isinstance(defender, Enemy):
                self.current_level.enemies.remove(defender)
            elif isinstance(defender, Character):
                self.is_game_over = True

    def _update_enemies_turn(self):
        for enemy in self.current_level.enemies:
            if self.player.health <= 0:
                break
            if enemy.enemy_type == "ogre" and enemy.is_resting == True:
                enemy.is_resting = False
                continue
            if abs(enemy.x - self.player.x) + abs(enemy.y - self.player.y) == 1:
                self.process_combat(enemy, self.player)

    def get_free_cell_around(self, start_x: int, start_y: int) -> tuple [int, int]:
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        for dx,dy in directions:
            x = start_x + dx
            y = start_y + dy
            is_walkable = self.current_level.is_walkable(x, y)
            is_free = True
            for item in self.current_level.items:
                if item.x == x and item.y == y:
                    is_free = False
                    break
            
            if is_free and is_walkable:
                return x, y
        return start_x, start_y
    
    def use_backpack_item(self, item_type: str, index: int) -> bool:
        success, old_weapon = self.player.use_item_by_index(item_type, index)
        if success == False:
            return success
        if old_weapon is not None:
            drop_x, drop_y = self.get_free_cell_around(self.player.x, self.player.y)
            old_weapon.x = drop_x
            old_weapon.y = drop_y
            self.current_level.items.append(old_weapon)
        if item_type == "food":
            self.food_eaten += 1
        self._update_enemies_turn()
        return success
            