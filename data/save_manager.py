import json
import os

class SaveManager:
    def __init__(self, savefile_path: str = "gamesave.json"): # ../player/
        self.savefile_path = savefile_path
        self.directory_name = os.path.dirname(self.savefile_path)
        self.last_index = self.get_last_save_index(self.directory_name if self.directory_name else ".")

        current_index = self.last_index if self.last_index > 0 else 1

        if self.directory_name:
            self.savefile_path = os.path.join(self.directory_name, f"gamesave_{current_index}.json")
        else:
            self.savefile_path = f"gamesave_{current_index}.json"
        

    @classmethod
    def get_last_save_index(cls, directory_path: str) -> int:
        if not os.path.exists(directory_path):
            return 0
        indexes = []
        for filename in os.listdir(directory_path):
            if filename.startswith("gamesave_") and filename.endswith(".json"):
                try:
                    num_str = filename[9:-5]
                    indexes.append(int(num_str))
                except ValueError:
                    continue
        return max(indexes) if indexes else 0


    def save_game(self, session_data: dict) -> bool:
        try:
            if self.directory_name and not os.path.exists(self.directory_name):
                os.makedirs(self.directory_name)
            
            write_index = self.last_index + 1
            self.last_index = write_index

            if self.directory_name:
                write_path = os.path.join(self.directory_name, f"gamesave_{write_index}.json")
            else:
                write_path = f"gamesave_{write_index}.json"

            with open(write_path, "w", encoding="utf-8") as file:
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
        
    def delete_save(self) -> bool:
        try:
            if not self.directory_name or not os.path.exists(self.directory_name):
                return False
                
            deleted_any = False
            for filename in os.listdir(self.directory_name):
                if filename.startswith("gamesave_") and filename.endswith(".json"):
                    full_path = os.path.join(self.directory_name, filename)
                    os.remove(full_path)
                    deleted_any = True
                    
            return deleted_any
        except Exception:
            return False
