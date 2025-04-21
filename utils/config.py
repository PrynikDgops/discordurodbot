import logging
import aiofiles
import json
import os
from typing import Dict, Any, Optional

from utils import classes

logger = logging.getLogger(__name__)
BOT_CONFIG_PATH = "./utils/bot_config.json"

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

def setup_config() -> Optional[classes.BotConfig]:
    with open(file=BOT_CONFIG_PATH, mode="r", encoding="utf-8") as file:
        config_data = json.loads(file.read())

    if not config_data:
        logger.error("No bot config data present!")
        return None

    main_guild_id = config_data["main_guild_id"]
    city_member_role_id = config_data["city_member_role_id"]
    probation_role_id = config_data["probation_role_id"]
    report_channel_id = config_data["report_channel_id"]
    log_channel_id = config_data["log_channel_id"]
    owner_id = config_data["owner_id"]
    deputy_role_id = config_data["deputy_role_id"]
    guardian_role_id = config_data["guardian_role_id"]
    big_city_member_role_id = config_data["big_city_member_role_id"]
    members_count_channel_id = config_data["members_count_channel_id"]
    head_role_id = config_data["head_role_id"]

    return classes.BotConfig(
        main_guild_id=main_guild_id,
        city_member_role_id=city_member_role_id,
        probation_role_id=probation_role_id,
        report_channel_id=report_channel_id,
        log_channel_id=log_channel_id,
        owner_id=owner_id,
        deputy_role_id=deputy_role_id,
        guardian_role_id=guardian_role_id,
        big_city_member_role_id=big_city_member_role_id,
        members_count_channel_id=members_count_channel_id,
        head_role_id=head_role_id,
    )


async def update_config_data(
    bot_config: classes.BotConfig, **kwargs
) -> Optional[classes.BotConfig]:
    async with aiofiles.open(file=BOT_CONFIG_PATH, mode="r", encoding="utf-8") as file:
        data = json.loads(await file.read())

    if not data:
        logger.error("No bot config data present!")
        return bot_config

    for key, value in kwargs.items():
        if key not in data:
            logger.warning(f"{key} is not in config parameters!")
            continue

        data[key] = value
        setattr(bot_config, key, value)

    async with aiofiles.open(file=BOT_CONFIG_PATH, mode="w", encoding="utf-8") as file:
        await file.write(json.dumps(data))

    return bot_config