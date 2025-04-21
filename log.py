import logging
import logging.handlers
import sys
from pathlib import Path
import settings

import coloredlogs


def setup() -> None:
    format_string = "[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s"
    log_format = logging.Formatter(format_string)
    root_logger = logging.getLogger()

    if settings.DEBUG_MODE:
        root_logger.setLevel(logging.DEBUG)
        log_file = Path("./debug.log")
    else:
        root_logger.setLevel(logging.INFO)
        log_file = Path("./Bot.log")

    log_file.parent.mkdir(exist_ok=True)

    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * (2**20),
        backupCount=10,
        encoding="utf-8",
    )
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)

    logging.getLogger("disnake").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("disnake.http").setLevel(logging.ERROR)

    coloredlogs.DEFAULT_LEVEL_STYLES = {
        **coloredlogs.DEFAULT_LEVEL_STYLES,
        "trace": {"color": 246},
        "critical": {"background": "red"},
        "debug": coloredlogs.DEFAULT_LEVEL_STYLES["info"],
    }

    coloredlogs.DEFAULT_LOG_FORMAT = format_string

    coloredlogs.install(level=logging.INFO, stream=sys.stdout)