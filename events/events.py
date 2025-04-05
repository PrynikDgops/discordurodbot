from disnake.ext import commands # type: ignore
from utils.config import load_config

config = load_config()

class BotEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.auto_report_task = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Бот запущен как {self.bot.user}")
        if config.get("auto_report_enabled", False):
            await self.start_auto_report()

def setup(bot: commands.Bot):
    bot.add_cog(BotEvents(bot))