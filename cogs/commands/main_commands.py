import logging
import disnake
from disnake.ext import commands

from utils import database, sync_functions
from utils.ui import tasks
from embeds import build_embed
import settings


logger = logging.getLogger(__name__)


async def no_permission_message(inter: disnake.ApplicationCommandInteraction):
    await inter.edit_original_response(
        embed=build_embed(
            description="У вас недостаточно прав для использования этой команды!",
            failure=True,
        )
    )


class MainCommands(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="создать-задание",
        description="Создать сообщение с заданием",
        dm_permission=False,
    )
    @commands.default_member_permissions(administrator=True)
    async def create_task(self, inter: disnake.ApplicationCommandInteraction):
        role = await settings.BOT_CONFIG.get_head_role(bot=self.bot)
        if (
            role not in inter.author.roles
            and inter.author.id != 302065849722732544
        ):
            return await inter.response.send_message(
                embed=build_embed(
                    description="У вас недостаточно прав для использования этой команды!",
                    failure=True,
                ),
                ephemeral=True,
            )

        await inter.response.send_modal(tasks.NewTask())

    @commands.message_command(name="Закончить задание", dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    async def finish_task(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        message: disnake.Message,
    ):
        await interaction.response.defer(ephemeral=True)
        role = await settings.BOT_CONFIG.get_head_role(bot=self.bot)
        if (
            role not in interaction.author.roles
            and interaction.author.id != 302065849722732544
        ):
            return await no_permission_message(inter=interaction)

        task_data = await database.get_task(message_id=message.id)
        if not task_data:
            return await interaction.edit_original_response(
                embed=build_embed(
                    description="Данное сообщение не является заданием!", failure=True
                )
            )

        await database.remove_task(message_id=message.id)

        embeds = [
            message.embeds[0],
            build_embed(description="### ✅ Задание выполнено!", without_title=True),
        ]

        await message.edit(embeds=embeds, view=None)

        await interaction.edit_original_response(
            embed=build_embed("Задание успешно закрыто!")
        )


def setup(bot: commands.Bot):
    bot.add_cog(MainCommands(bot))
    logger.info(f">{__name__} is launched")