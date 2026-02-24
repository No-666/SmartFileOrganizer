import yaml
from pathlib import Path
from typing import Dict, Any

DEFAULT_CONFIG: Dict[str, Any] = {
    "rules": [
        {"type": "extension", "values": [".jpg", ".jpeg", ".png", ".gif", ".heic"], "folder": "Media/Photos/{year}/{month}"},
        {"type": "extension", "values": [".mp4", ".mov", ".avi", ".mkv"], "folder": "Media/Videos/{year}"},
        {"type": "extension", "values": [".pdf", ".doc", ".docx", ".txt", ".md"], "folder": "Documents/{year}"},
        {"type": "name_pattern", "pattern": "invoice", "folder": "Finance/Invoices"}
    ],
    "default_folder": "Others/{year}",
    "log_level": "INFO",
    "use_threads": True,
    "max_workers": 8
}

def load_config(config_path: str | None = None) -> Dict[str, Any]:
    if config_path and Path(config_path).exists():
        with open(config_path, encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        return {**DEFAULT_CONFIG, **user_config}
    return DEFAULT_CONFIG.copy()

def save_config(config: Dict, config_path: str):
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)