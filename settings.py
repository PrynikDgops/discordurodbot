from dotenv import load_dotenv, find_dotenv
import logging
import os

from utils import config

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)

DEBUG_MODE = True

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
if not BOT_TOKEN:
    logger.critical("Bot token not defined!")

BOT_CONFIG = config.setup_config()