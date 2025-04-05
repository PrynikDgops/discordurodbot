import disnake # type: ignore
from disnake.ext import commands # type: ignore
from utils.config import load_config, save_config

config = load_config()

class SettingsCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="установить-время-работы", description="Устанавливает требуемое время работы (часы).",)
    async def set_required_work_time(inter: disnake.ApplicationCommandInteraction, hours: float):
        config["required_work_time_hours"] = hours
        save_config(config)
        await inter.response.send_message(f"Требуемое время работы установлено: {hours} часов.", ephemeral=True)
        
    @commands.slash_command(name="установить-период-работы", description="Устанавливает период проверки отчетности (часы).",)
    @commands.check(allowed_check) # type: ignore
    async def set_report_check_period(
        inter: disnake.ApplicationCommandInteraction, hours: float):
        config["report_check_period_hours"] = hours
        save_config(config)
        await inter.response.send_message(f"Период проверки отчетности установлен: {hours} часов.", ephemeral=True)
        pass

def setup(bot: commands.Bot):
    bot.add_cog(SettingsCommands(bot))