import disnake # type: ignore
from disnake.ext import commands # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

# Инициализация бота
bot = commands.InteractionBot(intents=disnake.Intents.default())

# Загрузка модулей
bot.load_extension("events.events")
bot.load_extension("events.errors")
bot.load_extension("cogs.admin")
bot.load_extension("cogs.whitelist")
bot.load_extension("cogs.reports")
bot.load_extension("cogs.voice")
bot.load_extension("cogs.settings")

# Запуск бота
if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))