import disnake
import logging
from disnake.ext import commands

import settings
from utils import database
from embeds import build_embed


logger = logging.getLogger(__name__)

VERIFY_CUSTOM_EMBED_TEXT = "(Вам придётся ввести команду заново для отправки сообщения)"


class ButtonsCallback(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener(name=disnake.Event.button_click)
    async def take_task(self, interaction: disnake.MessageInteraction):
        if interaction.data["custom_id"] != "take-task":
            return

        await interaction.response.defer(with_message=True, ephemeral=True)

        task_workers = await database.get_task_workers(
            message_id=interaction.message.id
        )
        task = await database.get_task(message_id=interaction.message.id)

        if interaction.author.id in task_workers:
            return await interaction.edit_original_response(
                embed=build_embed(
                    description="Вы уже выполняете данное задание!",
                    failure=True,
                )
            )

        await database.add_worker(
            message_id=interaction.message.id, user_id=interaction.author.id
        )

        embed = build_embed(
            description=f"### **Задание выполняют:** {len(task_workers) + 1} {'урод' if len(task_workers) + 1 == 1 else 'урода'}",
            color=disnake.Color.from_rgb(r=26, g=2, b=2),
            without_title=True,
        )

        embeds = interaction.message.embeds
        embeds[1] = embed
        await interaction.message.edit(embeds=embeds)

        log_channel = await settings.BOT_CONFIG.get_log_channel(bot=interaction.bot)
        owner = await settings.BOT_CONFIG.get_owner(bot=interaction.bot)

        description = f"{interaction.author.mention} взялся за задание [**{interaction.message.embeds[0].title}**]({interaction.message.jump_url})!\n"
        
        description += f"**Над заданием работают:** {len(task_workers) + 1} {'урод' if len(task_workers) + 1 == 1 else 'урода'}!"

        await log_channel.send(
            owner.mention,
            embed=build_embed(
                description=description,
                without_title=True,
            ),
        )

        await interaction.edit_original_response(
            embed=build_embed(description="Вы успешно взяли задание!")
        )

    @commands.Cog.listener(name=disnake.Event.button_click)
    async def send_embed(self, interaction: disnake.MessageInteraction):
        if interaction.data["custom_id"] != "send-embed":
            return

        await interaction.response.defer(ephemeral=True)
        embed = interaction.message.embeds[0]

        content = interaction.message.content if interaction.message.content else None

        await interaction.channel.send(
            embed=(
                embed
                if not embed.description
                or VERIFY_CUSTOM_EMBED_TEXT not in embed.description
                or embed.image
                else None
            ),
            content=content if content is not None else None,
        )

        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                label="Отправлено", style=disnake.ButtonStyle.green, disabled=True
            )
        )

        await interaction.edit_original_response(
            embed=build_embed(description="Сообщение успешно отправлено!"), view=view
        )

    @commands.Cog.listener(name=disnake.Event.button_click)
    async def reject_embed(self, interaction: disnake.MessageInteraction):
        if interaction.data["custom_id"] != "reject-embed":
            return

        await interaction.response.defer(ephemeral=True)

        description = "Отправка отменена. Можете скопировать старые данные ниже, если хотите отредактировать текст!\n\n"

        description += (
            ("**Ваше сообщение:**\n```" + interaction.message.content + "```\n\n")
            if interaction.message.content
            else ""
        )

        old_embed = interaction.message.embeds[0]
        is_custom_embed = (
            not old_embed.description
            or VERIFY_CUSTOM_EMBED_TEXT not in old_embed.description
        )

        if is_custom_embed:
            description += (
                ("**Заголовок эмбеда:**\n```" + old_embed.title + "```\n\n")
                if old_embed.title
                else ""
            )
            description += (
                ("**Текст эмбеда:**\n```" + old_embed.description + "```\n\n")
                if old_embed.description
                else ""
            )

            description += (
                ("**Картинка эмбеда:**\n```" + old_embed.image.url + "```")
                if old_embed.image
                else ""
            )

        embed = disnake.Embed(
            title="СТАРЫЙ ЭМБЕД", description=description, color=disnake.Color.orange()
        )

        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                label="Отменено", style=disnake.ButtonStyle.red, disabled=True
            )
        )

        await interaction.edit_original_response(embed=embed, view=view, content=None)


def setup(bot: commands.bot):
    bot.add_cog(ButtonsCallback(bot))
    logger.info(f">{__name__} is launched")