import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os
from bot import UrodCityPointer
import settings

import log

load_dotenv()

# Инициализация бота
bot = UrodCityPointer().create()

# Загрузка модулей
bot.load_extension("events.events")
bot.load_extension("events.errors")
bot.load_extensions("cogs")
bot.remove_command("help")

# Запуск бота
if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))