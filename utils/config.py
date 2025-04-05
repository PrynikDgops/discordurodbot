import json
import os
from typing import Dict, Any

CONFIG_FILE = "config.json"

def load_config() -> Dict[str, Any]:
    default_config = {
        "required_work_time_hours": 1.5,
        "report_check_period_hours": 48,
        "applicable_roles": [],
        "auto_report_enabled": False,
        "auto_report_channel": None,
        "command_access_users": [],
        "command_access_roles": [],
        "whitelist": [],
    }
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                return {**default_config, **config}
        except (json.JSONDecodeError, FileNotFoundError):
            return default_config
    return default_config

def save_config(config: Dict[str, Any]) -> None:
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)