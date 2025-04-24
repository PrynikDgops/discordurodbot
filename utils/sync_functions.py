import disnake
from disnake.ext import commands
import datetime

import settings
from embeds import build_embed
from utils import database



async def setup_database(bot: commands.Bot) -> None:
    city_member_role = await settings.BOT_CONFIG.get_city_member_role(bot=bot)
    probation_role = await settings.BOT_CONFIG.get_probation_role(bot=bot)
    deputy_role = await settings.BOT_CONFIG.get_deputy_role(bot=bot)
    guardian_role = await settings.BOT_CONFIG.get_guardian_role(bot=bot)
    big_city_member_role = await settings.BOT_CONFIG.get_big_city_member_role(bot=bot)

    members = (
        city_member_role.members
        + probation_role.members
        + deputy_role.members
        + guardian_role.members
        + big_city_member_role.members
    )
    discord_member_ids = [member.id for member in members]

    current_database_members = await database.get_all_users()
    current_database_member_ids = [
        member.discord_id for member in current_database_members
    ]

    #  Обрабатываем прямую синхронизацию
    for member_id in discord_member_ids:
        if member_id not in current_database_member_ids:
            await database.add_user_if_not_exists(discord_id=member_id)

    #  Обрабатываем обратную синхронизацию
    for member_id in current_database_member_ids:
        if member_id not in discord_member_ids:
            await database.remove_member(discord_id=member_id)