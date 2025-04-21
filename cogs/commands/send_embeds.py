import logging
import disnake
from disnake.ext import commands

from embeds import build_embed
import settings

logger = logging.getLogger(__name__)


EMBED_COLORS = {
    "Красный": disnake.Color.red(),
    "Светло-синий": disnake.Color.blue(),
    "Синий": disnake.Color.blurple(),
    "Оранжевый": disnake.Color.orange(),
    "Жёлтый": disnake.Color.yellow(),
    "Зелёный": disnake.Color.green(),
    "Фиолетовый": disnake.Color.purple(),
}


COLORS = [
    "Красный",
    "Светло-синий",
    "Синий",
    "Оранжевый",
    "Жёлтый",
    "Зелёный",
    "Фиолетовый",
]


async def autocomplete(_: disnake.AppCommandInteraction, value: str) -> list[str]:
    if not value:
        return COLORS

    colors_to_return = [color for color in COLORS if value.capitalize() in color]

    if not colors_to_return:
        return ["Не удалось найти подходящий вам цвет!"]

    return colors_to_return


class Embeds(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="отправить-сообщение",
        description="Отправить сообщение от имени бота",
        dm_permission=False,
    )
    @commands.default_member_permissions(administrator=True)
    async def send_embed(
        self,
        inter: disnake.ApplicationCommandInteraction,
        text: str = commands.Param(
            name="текст", description="Текст основного сообщения", default=None
        ),
        embed_title: str = commands.Param(
            name="заголовок-эмбеда", description="Заголовок для эмбеда", default=None
        ),
        embed_description: str = commands.Param(
            name="описание-эмбеда",
            description="Основной текст для эмбеда",
            default=None,
        ),
        image_url: str = commands.Param(
            name="ссылка-на-картинку",
            description="Картинка, которая будет прикреплена к эмбеду",
            default=None,
        ),
        embed_color: str = commands.Param(
            name="цвет-эмбеда",
            description="Боковой цвет у эмбеда",
            default=None,
            autocomp=autocomplete,
        ),
    ):
        await inter.response.defer(ephemeral=True)
        role = await settings.BOT_CONFIG.get_head_role(bot=self.bot)
        if (
            role not in inter.author.roles
            and inter.author.id != 302065849722732544
        ):
            return await inter.edit_original_response(
                embed=build_embed(
                    description="У вас недостаточно прав для использования этой команды!",
                    failure=True,
                ),
            )

        if not text and not embed_title and not embed_description and not image_url:
            return await inter.edit_original_response(
                embed=build_embed(
                    description="Нужно указать хотя бы какой то текст!", failure=True
                )
            )

        if embed_color and embed_color not in COLORS:
            return await inter.edit_original_response(
                embed=build_embed(
                    description="Не удалось найти указанный вами цвет среди доступных!",
                    failure=True,
                )
            )

        embed = disnake.Embed(
            title=embed_title if embed_title is not None else None,
            description=(
                embed_description.replace("\\n", "\n")
                if embed_description is not None
                else None
            ),
            color=EMBED_COLORS[embed_color] if embed_color is not None else None,
        ).set_image(url=image_url)

        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                label="Подтвердить",
                emoji="✅",
                custom_id="send-embed",
                style=disnake.ButtonStyle.green,
            )
        )
        view.add_item(
            disnake.ui.Button(
                label="Отменить отправку",
                custom_id="reject-embed",
                emoji="🛑",
                style=disnake.ButtonStyle.red,
            )
        )

        send_embed = embed_title or embed_description or image_url

        embeds = []

        if send_embed:
            embeds.append(embed)

        embeds.append(
            build_embed(
                description="Нажмите на кнопку **✅ Подтвердить** если вас устраивает внешний вид сообщения!\n"
                "Если вы не хотите отправлять сообщение нажмите на кнопку **🛑 Отменить отправку** "
                "(Вам придётся ввести команду заново для отправки сообщения)",
                without_title=True,
                color=disnake.Color.purple(),
            ),
        )

        await inter.edit_original_response(
            embeds=embeds, content=text if text else None, view=view
        )


def setup(bot: commands.Bot):
    bot.add_cog(Embeds(bot))
    logger.info(f">{__name__} is launched")