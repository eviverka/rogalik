import random

from entities import *

class Room:
    def __init__(self, start_x: int, start_y: int, width: int, height: int):
        self.x = start_x
        self.y = start_y
        self.width = width
        self.height = height
    
    def has_point(self, check_x: int, check_y: int) -> bool:
        right_border = self.x + self.width
        bottom_border = self.y + self.height

        is_inside_x = self.x <= check_x < right_border
        is_inside_y = self.y <= check_y < bottom_border
        is_inside = is_inside_x and is_inside_y

        return is_inside

class Corridor:
    def __init__(self, points: set = None):
        if points is None:
            self.points = set()
        else:
            self.points = points

    def has_point(self, check_x: int, check_y: int) -> bool:
        current_point = (check_x, check_y)
        is_inside = current_point in self.points
        return is_inside
    
class Level:
    def __init__(self, level_index: int):
        self.index = level_index
        self.rooms: list[Room] = []
        self.corridors: list[Corridor] = []
        self.enemies: list[Enemy] = []
        self.items: list[Item] = []
        self.exit_x: int = 0
        self.exit_y: int = 0
        self.discovered_cells: set[tuple[int,int]] = set()

    def is_walkable(self, x: int, y: int) -> bool:
        return any(room.has_point(x, y) for room in self.rooms) or any(corridor.has_point(x, y) for corridor in self.corridors)
    
    def is_exit(self, x: int, y: int) -> bool:
        return self.exit_x == x and self.exit_y == y
    
    def get_line(self, x1: int, y1: int, x2: int, y2: int) -> list[tuple[int, int]]:
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        dir_x = 1 if x1 < x2 else -1
        dir_y = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            points.append((x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += dir_x
            if e2 < dx:
                err += dx
                y1 += dir_y
                
        return points

    def update_visibility(self, player: Character, R: int = 7):
        for ty in range(player.y - R, player.y + R + 1):
            for tx in range(player.x - R, player.x + R + 1):
                if ty == player.y - R or ty == player.y + R or tx == player.x - R or tx == player.x + R:
                    line = self.get_line(player.x, player.y, tx, ty)
                    for lx, ly in line:
                        self.discovered_cells.add((lx, ly))
                        if not self.is_walkable(lx, ly):
                            break


class LevelGenerator:
    def __init__(self, map_width: int = 80, map_height: int = 24):
        self.map_width = map_width
        self.map_height = map_height
        self.sector_width = self.map_width // 3
        self.sector_height = self.map_height // 3

    def generate_rooms(self, level: Level):
        for row in range(3):
            for col in range(3):
                start_sector_x = col * self.sector_width
                start_sector_y = row * self.sector_height
                room_width = random.randint(5, self.sector_width - 2)
                room_height = random.randint(4, self.sector_height - 2)
                max_offset_x = self.sector_width - room_width
                max_offset_y = self.sector_height - room_height
                offset_x = random.randint(1, max_offset_x - 1)
                offset_y = random.randint(1, max_offset_y - 1)
                room_x = start_sector_x + offset_x
                room_y = start_sector_y + offset_y
                new_room = Room(room_x, room_y, room_width, room_height)
                level.rooms.append(new_room)
        
    def generate_corridors(self, level: Level):
        while True:
            room_graph = {i: [] for i in range(9)}
            visited = set()

            def dfs(node):
                visited.add(node)
                for neighbor in room_graph[node]:
                    if neighbor not in visited:
                        dfs(neighbor)
            
            for i in range(9):
                row = i // 3
                col = i % 3
                if col < 2:
                    right_neighbor = i + 1
                    if random.choice([True, False]):
                        self.add_relation(room_graph, i, right_neighbor)
                if row < 2:
                    bottom_neighbor = i + 3
                    if random.choice([True, False]):
                        self.add_relation(room_graph, i, bottom_neighbor)

            dfs(0)
            if len(visited) == 9:
                break
        for i in range(9):
            for neighbor in room_graph[i]:
                if i < neighbor:
                    room_a = level.rooms[i]
                    room_b = level.rooms[neighbor]
                    ax = room_a.x + room_a.width // 2
                    ay = room_a.y + room_a.height // 2
                    bx = room_b.x + room_b.width // 2
                    by = room_b.y + room_b.height // 2
                    corridor_points = set()
                    start_x = min(ax, bx)
                    end_x = max(ax, bx)
                    for x in range(start_x, end_x + 1):
                        corridor_points.add((x, ay))
                    start_y = min(ay, by)
                    end_y = max(ay, by)
                    for y in range(start_y, end_y + 1):
                        corridor_points.add((bx, y))
                    new_corridor = Corridor(corridor_points)
                    level.corridors.append(new_corridor)


    def add_relation(self, graph, node_a: int, node_b: int):
        if node_b not in graph[node_a]:
            graph[node_a].append(node_b)
        if node_a not in graph[node_b]:
            graph[node_b].append(node_a)
    
    def place_start_and_exit(self, level: Level) -> tuple:
        start_room, end_room = random.sample(level.rooms, 2)
        player_start_x = random.randint(start_room.x + 1, start_room.x + start_room.width - 2)
        player_start_y = random.randint(start_room.y + 1, start_room.y + start_room.height - 2)
        level.exit_x = random.randint(end_room.x + 1, end_room.x + end_room.width - 2)
        level.exit_y = random.randint(end_room.y + 1, end_room.y + end_room.height - 2)
        return player_start_x, player_start_y
    
    def build_level(self, level_index: int) -> tuple[Level, int, int]:
        level = Level(level_index)
        self.generate_rooms(level)
        self.generate_corridors(level)
        player_x, player_y = self.place_start_and_exit(level)
        return level, player_x, player_y