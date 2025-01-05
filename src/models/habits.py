import json
import os
from typing import List, Dict

class Habits:
    def __init__(self, path) -> None:
        self._file_path = os.path.join(path, 'habits.json')
        self._habits = self._load_from_file()
        self._inactive = {}
        if not self._habits:  # Initialize with a default habit if the file is empty
            self._habits = {
                "CONFIDENCE": "Please grade your confidence in the response, being transparent about any uncertainty. The confidence score should be a single score in format **Confidence 0-99** at the end of the content.",
                "TAGGING": "Please add relevant tags about the topic of conversation to the bottom of the response given. The tags should be concise and written under a **Tags** flag for organization."
            }
            self._save_to_file(self._habits)
    
    def _load_from_file(self) -> Dict[str, str]:
        try:
            with open(self._file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
    
    def _save_to_file(self, habits: Dict[str, str]) -> None:
        with open(self._file_path, 'w') as file:
            json.dump(habits, file, indent=4)
    
    def load(self) -> List[str]:
        return list(self._habits.values())

    def active(self) -> List[str]:
        return list(self._habits.keys())

    def inactive(self) -> List[str]:
        return list(self._inactive.keys())

    def toggle(self, name):
        key = name.upper()
        if key in self._habits:
            self._inactive[key] = self._habits[key]
            self._habits.pop(key)
        elif key in self._inactive:
            self._habits[key] = self._inactive[key]
            self._inactive.pop(key)

    def toggle_all(self, enable: bool):
        if enable:
            # Enable all habits: Move all from _inactive to _habits
            self._habits.update(self._inactive)
            self._inactive.clear()
        else:
            # Disable all habits: Move all from _habits to _inactive
            self._inactive.update(self._habits)
            self._habits.clear()

    def add(self, name: str, description: str) -> None:
        key = name.upper()
        if key in self._habits:
            raise ValueError(f"Habit '{name}' already exists.")
        self._habits[key] = description
        self._save_to_file(self._habits)

    def get_habit(self, name: str) -> str:
        return self._habits.get(name.upper(), "Habit not found")

    def __str__(self) -> str:
        return '\033[33mActive:\033[0m\n'+'\n'.join([f"{key}" for key, _ in self._habits.items()])+'\n\033[33mInactive:\033[0m\n'+'\n'.join([f"{key}" for key, _ in self._inactive.items()])
