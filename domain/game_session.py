import random

from collections import deque
from domain.entities import *
from domain.map import *

class GameSession:
    def __init__(self, player: Character, current_level: Level, level_generator: LevelGenerator):
        self.player = player
        self.current_level = current_level
        self.level_generator = level_generator
        self.steps_passed: int = 0
        self.enemies_killed: int = 0
        self.food_eaten: int = 0
        self.is_game_over = False
        self.is_victory = False
        self.current_level.update_visibility(self.player)

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

        if self.current_level.is_exit(self.player.x, self.player.y):
            if self.current_level.index == 21:
                self.is_victory = True
                return
            else:
                next_index = self.current_level.index + 1
                new_level, px, py = self.level_generator.build_level(next_index)
                self.current_level = new_level
                self.player.x = px
                self.player.y = py
                self.current_level.update_visibility(self.player)
                return
        self.current_level.update_visibility(self.player)
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
                self.enemies_killed += 1
            elif isinstance(defender, Character):
                self.is_game_over = True

    def _update_enemies_turn(self):
        for enemy in self.current_level.enemies:
            if self.player.health <= 0:
                break

            if enemy.enemy_type == "ogre" and enemy.is_resting == True:
                enemy.is_resting = False
                continue

            distance = abs(enemy.x - self.player.x) + abs(enemy.y - self.player.y)

            if enemy.enemy_type == "ghost":
                if distance <= enemy.hostility:
                    enemy.is_invisible = False
                else:
                    if random.randint(1, 100) <= 40:
                        enemy.is_invisible = not enemy.is_invisible
                        
            if distance == 1:
                self.process_combat(enemy, self.player)
            elif distance <= enemy.hostility:
                nx, ny = self.get_next_step(enemy)
                enemy.x = nx
                enemy.y = ny
            elif distance > enemy.hostility:
                nx, ny = self.make_random_move(enemy)
                enemy.x = nx
                enemy.y = ny
        self.current_level.update_visibility(self.player)

    def get_next_step(self, enemy: Enemy) -> tuple [int, int]:
        queue = deque([(enemy.x, enemy.y)])
        visited = set()
        parent = {}
        found = False
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            current = queue.popleft()
            cx, cy = current

            for dx, dy in directions:
                nx, ny = cx+dx, cy+dy
                neighbor = (nx, ny)

                if nx == self.player.x and ny == self.player.y:
                    parent[neighbor] = current
                    curr = (self.player.x, self.player.y)
                    while parent.get(curr) != (enemy.x, enemy.y):
                        curr = parent[curr]
                    return curr

                if self.current_level.is_walkable(nx, ny) and neighbor not in visited:
                    if not any(e.x == nx and e.y == ny for e in self.current_level.enemies):
                        visited.add(neighbor)
                        parent[neighbor] = current
                        queue.append(neighbor)

        return enemy.x, enemy.y
    
    def make_random_move(self, enemy: Enemy) -> tuple[int, int]:
        def cell_is_free(x: int, y: int) -> bool:
            return self.current_level.is_walkable(x, y) and not any(e.x == x and e.y == y for e in self.current_level.enemies)
        
        cross_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        diagonal_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        if enemy.enemy_type == "ghost":
            ghost_room = None
            for room in self.current_level.rooms:
                if room.has_point(enemy.x, enemy.y):
                    ghost_room = room
                    break
            
            for _ in range(10):
                tx = random.randint(ghost_room.x + 1, ghost_room.x + ghost_room.width - 2)
                ty = random.randint(ghost_room.y + 1, ghost_room.y + ghost_room.height - 2)
                if cell_is_free(tx, ty):
                    return tx, ty
            return enemy.x, enemy.y

        if enemy.enemy_type == "snake_mage":
            valid_dirs = [(dx, dy) for dx, dy in diagonal_directions if cell_is_free(enemy.x + dx, enemy.y + dy)]
        elif enemy.enemy_type == "ogre":
            valid_dirs = [(dx, dy) for dx, dy in cross_directions if cell_is_free(enemy.x + dx, enemy.y + dy) and cell_is_free(enemy.x + dx*2, enemy.y + dy*2)]
        else:
            valid_dirs = [(dx, dy) for dx, dy in cross_directions if cell_is_free(enemy.x + dx, enemy.y + dy)]

        if valid_dirs:
            dx, dy = random.choice(valid_dirs)
            if enemy.enemy_type == "ogre":
                return enemy.x + dx * 2, enemy.y + dy * 2
            return enemy.x + dx, enemy.y + dy

        return enemy.x, enemy.y


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

    def to_dict(self) -> dict:
        return {
            "steps_passed": self.steps_passed,
            "enemies_killed": self.enemies_killed,
            "food_eaten": self.food_eaten,
            "player": self.player.to_dict(),
            "level": self.current_level.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: dict, level_generator: LevelGenerator):
        player = Character.from_dict(data["player"])
        level = Level.from_dict(data["level"])
        session = cls(player, level, level_generator)
        session.steps_passed = data["steps_passed"]
        session.enemies_killed = data["enemies_killed"]
        session.food_eaten = data["food_eaten"]
        return session