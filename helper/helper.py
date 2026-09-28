import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STORAGE_PATH = PROJECT_ROOT / "src/storage"
print(STORAGE_PATH)


def get_table_path(table_name: str) -> Path:
    return STORAGE_PATH / f"{table_name}.json"


def load_table(table_name: str):
    with open(get_table_path(table_name), "r") as file:
        return json.load(file)


def save_table(table_name: str, data):
    with open(get_table_path(table_name), "w") as file:
        json.dump(data, file, indent=4)


def get_storage_path() -> Path:
    return STORAGE_PATH
