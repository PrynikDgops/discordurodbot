import disnake # type: ignore
from disnake.ext import commands # type: ignore
import asyncio
from utils.config import load_config, save_config
from utils.helpers import generate_report
from typing import Optional, Union


config = load_config()

class ReportCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.auto_report_task = None

    @commands.slash_command(name="проверить-отчеты", description="Проверяет отчетность в указанном канале.")
    async def check_reports(inter: disnake.ApplicationCommandInteraction, report_channel: disnake.TextChannel, period: Optional[float] = None):
        # Немедленно откладываем ответ, чтобы дать себе больше времени
        await inter.response.defer()
        if period is None:
            period = config.get("report_check_period_hours", 24)
        report = await generate_report(report_channel, period)
        # Редактируем первоначальный ответ, отправляя отчет
        await inter.edit_original_response(content=report)
        pass

def setup(bot: commands.Bot):
    bot.add_cog(ReportCommands(bot))