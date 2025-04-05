import disnake # type: ignore
from disnake.ext import commands # type: ignore
from disnake import HTTPException, NotFound # type: ignore
from disnake.ext.commands import MissingPermissions, Context # type: ignore

class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(inter: disnake.ApplicationCommandInteraction, error: commands.CommandError):
        try:
            if not inter.response.is_done():
                await inter.response.defer(ephemeral=True)
            await inter.followup.send(f"Ошибка: {error}", ephemeral=True)
        except NotFound:  # Игнорируем недействительные взаимодействия
            pass
        except HTTPException as e:
            print(f"Не удалось отправить сообщение об ошибке: {e}")
    
    @commands.Cog.listener()
    async def on_slash_command_error(inter: disnake.ApplicationCommandInteraction, error: Exception):
        if isinstance(error, MissingPermissions):
            await inter.response.send_message("Ошибка: недостаточно прав для использования этой команды.", ephemeral=True)
        else:
            await inter.response.send_message(f"Ошибка: {error}", ephemeral=True)
        pass

def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))