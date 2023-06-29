""" Functions to read and write from files in different formats.

    The priority here is on a functional programming style,
    focussing on readability and testability.
"""
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict


def read_text_file(file_path: Path) -> str:
    """Open and read a text file."""
    with open(file_path, 'r') as file_object:
        return file_object.read()


def read_json_file(file_path: Path) -> List[Dict]:
    """Open and read a JSON file."""
    with open(file_path, 'r') as file_object:
        return json.load(file_object)


def write_text_file(filepath: Path, content: str):
    """Write text content to a file."""
    with open(filepath, 'w') as file:
        file.write(content)


def write_csv_file(filepath: Path, content: Dict):
    """Write a list of dictionaries to a CSV file."""
    df = pd.DataFrame.from_dict(content)
    df.to_csv(filepath)


def write_json_file(filepath: Path, content: List[Dict]):
    """Write a list of dictionaries to a JSON file."""
    with open(filepath, 'w') as json_file_obj:
        json.dump(content, json_file_obj)


def fetch_all_file_paths(directory: str) -> List[Path]:
    """
    Function to fetch all file paths in a given directory.
    """
    directory_path = Path(directory)
    file_paths = [path for path in directory_path.glob('**/*') if path.is_file()]
    return file_paths
