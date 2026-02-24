import hashlib
import os
from datetime import datetime
from pathlib import Path
from typing import Dict

def get_file_hash(file_path: str, algo: str = "md5") -> str:
    hash_func = hashlib.md5() if algo == "md5" else hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def get_file_info(file_path: str) -> Dict:
    path = Path(file_path)
    stat = os.stat(file_path)
    dt = datetime.fromtimestamp(stat.st_mtime)
    return {
        "extension": path.suffix.lower(),
        "name": path.name.lower(),
        "size": stat.st_size,
        "year": dt.strftime("%Y"),
        "month": dt.strftime("%m"),
        "date": dt.strftime("%Y-%m-%d"),
        "mtime": stat.st_mtime
    }

def apply_rules(file_info: Dict, rules: list, default_folder: str) -> str:
    for rule in rules:
        if rule["type"] == "extension" and file_info["extension"] in [v.lower() for v in rule["values"]]:
            return rule["folder"].format(**file_info)
        if rule["type"] == "name_pattern" and rule["pattern"].lower() in file_info["name"]:
            return rule["folder"].format(**file_info)
    return default_folder.format(**file_info) if "{" in default_folder else default_folder