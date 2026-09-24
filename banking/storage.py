"""JSON file storage for bank accounts."""

import json
from pathlib import Path


class StorageError(Exception):
    """Raised when the data file cannot be read safely."""


class JSONStorage:
    """Read and write banking data in one local JSON file."""

    def __init__(self, file_path="data/accounts.json"):
        self.file_path = Path(file_path)

    def load(self):
        """Return saved data, creating an empty structure when needed."""
        if not self.file_path.exists():
            return {"accounts": {}}
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                content = file.read()
            if not content.strip():
                data = {"accounts": {}}
                self.save(data)
                return data
            data = json.loads(content)
        except json.JSONDecodeError as error:
            raise StorageError("The data file is not valid JSON.") from error
        except OSError as error:
            raise StorageError("Could not read the data file.") from error

        if not isinstance(data, dict) or not isinstance(data.get("accounts"), dict):
            raise StorageError("The data file has an invalid structure.")
        return data

    def save(self, data):
        """Save data, creating the data folder automatically."""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with self.file_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=2)
        except OSError as error:
            raise StorageError("Could not save the data file.") from error
