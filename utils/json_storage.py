"""
utils/json_storage.py
---------------------
Generic, thread-safe helpers for reading and writing JSON files.

All services that need persistence go through these two functions.
Swapping to a real database later only requires changing the service
layer — nothing else touches these helpers directly.
"""

import json
import os
from typing import Any


def read_json(filepath: str) -> Any:
    """
    Read and return the contents of a JSON file.

    If the file does not exist yet, return an empty dict so callers
    never have to handle a missing-file edge case on first run.

    Args:
        filepath: Absolute or relative path to the JSON file.

    Returns:
        Parsed Python object (dict, list, etc.).
    """
    if not os.path.exists(filepath):
        return {}

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(filepath: str, data: Any) -> None:
    """
    Serialise *data* and write it to *filepath*, creating the file
    (and any missing parent directories) if necessary.

    Args:
        filepath: Absolute or relative path to the target JSON file.
        data:     Any JSON-serialisable Python object.
    """
    parent = os.path.dirname(filepath)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
