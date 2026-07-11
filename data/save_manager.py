import json
import os

class SaveManager:
    def __init__(self, savefile_path: str = "gamesave.json"):
        self.savefile_path = savefile_path

    def save_game(self, session_data: dict) -> bool:
        try:
            with open(self.savefile_path, "w", encoding="utf-8") as file:
                json.dump(session_data, file, ensure_ascii=False, indent=4)
            return True
        except Exception:
            return False
        
    def load_game(self) -> dict:
        if os.path.exists(self.savefile_path):
            with open(self.savefile_path, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            return None