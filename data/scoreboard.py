import json
import os

from domain.game_session import *
from config import SCOREBOARD_FILE_PATH
class ScoreboardManager:
    def __init__(self):
        self.scoreboard_path = SCOREBOARD_FILE_PATH

    def _update_existing_record(self, record: dict, session: GameSession):
        record["gold"] = max(record["gold"], session.player.gold)
        record["steps_passed"] = max(record.get("steps_passed", 0), session.steps_passed)
        record["enemies_killed"] = max(record.get("enemies_killed", 0), session.enemies_killed)
        record["food_eaten"] = max(record.get("food_eaten", 0), session.food_eaten)

    def add_score(self, player_name: str, session: GameSession):
        leaderboard = self.load_scores()
        existing_record = None
        for record in leaderboard:
            if record["player_name"] == player_name:
                existing_record = record
                break
        
        if existing_record:
            self._update_existing_record(existing_record, session)
        else:
            new_result = {
                "player_name": player_name,
                "gold": session.player.gold,
                "steps_passed": session.steps_passed,
                "enemies_killed": session.enemies_killed,
                "food_eaten": session.food_eaten
            }
            leaderboard.append(new_result)
        leaderboard.sort(key=lambda x: x["gold"], reverse=True)
        leaderboard = leaderboard[:10]
        self.save_scores(leaderboard)

    def load_scores(self) -> list:
        if os.path.exists(self.scoreboard_path):
            with open(self.scoreboard_path, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            return []

    def _update_existing_record(self, record: dict, session: GameSession):
        record["gold"] = max(record["gold"], session.player.gold)
        record["steps_passed"] = max(record.get("steps_passed", 0), session.steps_passed)
        record["enemies_killed"] = max(record.get("enemies_killed", 0), session.enemies_killed)
        record["food_eaten"] = max(record.get("food_eaten", 0), session.food_eaten)

    def save_scores(self, scores: list) -> bool:
        try:
            folder_path = os.path.dirname(self.scoreboard_path)
            
            if folder_path:
                os.makedirs(folder_path, exist_ok=True)

            with open(self.scoreboard_path, "w", encoding="utf-8") as file:
                json.dump(scores, file, ensure_ascii=False, indent=4)
            return True
        except Exception:
            return False
