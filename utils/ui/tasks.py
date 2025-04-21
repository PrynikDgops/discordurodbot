import disnake

from utils import database
from embeds import build_embed
import settings


class NewTask(disnake.ui.Modal):
    def __init__(self):
        super().__init__(
            timeout=3000,
            title="НОВОЕ ЗАДАНИЕ",
            components=[
                disnake.ui.TextInput(
                    label="Заголовок",
                    placeholder="Пример: Добыча ресурсов",
                    custom_id="title",
                    style=disnake.TextInputStyle.short,
                ),
                disnake.ui.TextInput(
                    label="Описание задания",
                    placeholder="Пример: Идите туда, принесите то, вон туда вот!",
                    custom_id="description",
                    style=disnake.TextInputStyle.paragraph,
                    max_length=400,
                ),
                disnake.ui.TextInput(
                    label="Картинка",
                    placeholder="Пример: https://i.imgur.com/mrOn77R.png",
                    custom_id="image",
                    style=disnake.TextInputStyle.short,
                    required=False,
                ),

                disnake.ui.TextInput(
                    label="Обязательное задание",
                    placeholder="Пример: Да (или Нет)",
                    custom_id="required",
                    style=disnake.TextInputStyle.short,
                    min_length=2,
                    max_length=3,
                ),
            ],
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        await interaction.response.defer(with_message=True, ephemeral=True)
        title = interaction.text_values["title"]
        description = interaction.text_values["description"]
        try:
            image = interaction.text_values["image"]
        except KeyError:
            image = None
        required = interaction.text_values["required"]

        required = True if required.replace(" ", "").lower() == "да" else False

        description += (
            "\n**__ОБЯЗАТЕЛЬНОЕ ЗАДАНИЕ__**"
            if required
            else "\n**__НЕ ОБЯЗАТЕЛЬНО ЗАДАНИЕ__**"
        )

        embed = disnake.Embed(
            title=title,
            description=description,
            color=disnake.Color.from_rgb(r=255, g=3, b=3),
        )
        if image is not None:
            embed.set_image(url=image)

        member_role = await settings.BOT_CONFIG.get_city_member_role(
            bot=interaction.bot
        )
        probation_role = await settings.BOT_CONFIG.get_probation_role(
            bot=interaction.bot
        )
        deputy_role = await settings.BOT_CONFIG.get_deputy_role(bot=interaction.bot)
        guardian_role = await settings.BOT_CONFIG.get_guardian_role(bot=interaction.bot)
        big_city_member_role = await settings.BOT_CONFIG.get_big_city_member_role(
            bot=interaction.bot
        )

        view = None
        if not required:
            view = disnake.ui.View()
            view.add_item(
                disnake.ui.Button(
                    label="Взяться за задание",
                    style=disnake.ButtonStyle.green,
                    custom_id="take-task",
                )
            )

        embeds = [
            embed,
            build_embed(
                description="### **Задание выполняют:** 0 уродов",
                without_title=True,
                color=disnake.Color.from_rgb(r=26, g=2, b=2),
            ),
        ]

        message = await interaction.channel.send(
            member_role.mention
            + probation_role.mention
            + deputy_role.mention
            + guardian_role.mention
            + big_city_member_role.mention,
            embeds=embeds if not required else None,
            embed=embed if required else None,
            view=view,
        )

        await database.add_new_task(
            message_id=message.id,
            required=required,
        )

        await interaction.edit_original_response(
            embed=build_embed(description="Задание опубликовано!")
        )