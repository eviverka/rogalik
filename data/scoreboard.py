import json
import os

from domain.game_session import *
class ScoreboardManager:
    def __init__(self, scoreboard_path: str = "scoreboard.json"):
        self.scoreboard_path = scoreboard_path

    def add_score(self, player_name: str, session: GameSession):
        leaderboard = self.load_scores()
        existing_record = None
        for record in leaderboard:
            if record["player_name"] == player_name:
                existing_record = record
                break
        
        if existing_record:
            if session.player.gold <= existing_record["gold"]:
                return
            else:
                existing_record["gold"] = session.player.gold
                existing_record["steps_passed"] = session.steps_passed
                existing_record["enemies_killed"] = session.enemies_killed
                existing_record["food_eaten"] = session.food_eaten
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

    def save_scores(self, scores: list) -> bool:
        try:
            with open(self.scoreboard_path, "w", encoding="utf-8") as file:
                json.dump(scores, file, ensure_ascii=False, indent=4)
            return True
        except Exception:
            return False