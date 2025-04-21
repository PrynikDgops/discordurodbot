import logging
import disnake
from disnake.ext import commands

from utils import database
import settings

logger = logging.getLogger(__name__)


class Roles(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    @commands.Cog.listener(name=disnake.Event.audit_log_entry_create)
    async def on_audit_log_entry_create(self, entry: disnake.AuditLogEntry):
        if entry.action != disnake.AuditLogAction.member_role_update:
            return

        member_role = await settings.BOT_CONFIG.get_city_member_role(bot=self.bot)
        probation_role = await settings.BOT_CONFIG.get_probation_role(bot=self.bot)
        deputy_role = await settings.BOT_CONFIG.get_deputy_role(bot=self.bot)
        guardian_role = await settings.BOT_CONFIG.get_guardian_role(bot=self.bot)
        big_city_member_role = await settings.BOT_CONFIG.get_big_city_member_role(
            bot=self.bot
        )

        if (
            (member_role not in entry.before.roles and member_role in entry.after.roles)
            or (
                probation_role not in entry.before.roles
                and probation_role in entry.after.roles
            )
            or (
                deputy_role not in entry.before.roles
                and deputy_role in entry.after.roles
            )
            or (
                guardian_role not in entry.before.roles
                and guardian_role in entry.after.roles
            )
            or (
                big_city_member_role not in entry.before.roles
                and big_city_member_role in entry.after.roles
            )
        ):
            await database.add_user_if_not_exists(discord_id=entry.target.id)
        elif member_role in entry.before.roles and member_role not in entry.after.roles:
            if (
                probation_role not in entry.target.roles
                and deputy_role not in entry.target.roles
                and guardian_role not in entry.target.roles
                and big_city_member_role not in entry.target.roles
            ):
                await database.remove_member(discord_id=entry.target.id)
        elif (
            probation_role in entry.before.roles
            and probation_role not in entry.after.roles
        ):
            if (
                member_role not in entry.target.roles
                and deputy_role not in entry.target.roles
                and guardian_role not in entry.target.roles
                and big_city_member_role not in entry.target.roles
            ):
                await database.remove_member(discord_id=entry.target.id)
        elif deputy_role in entry.before.roles and deputy_role not in entry.after.roles:
            if (
                member_role not in entry.target.roles
                and probation_role not in entry.target.roles
                and guardian_role not in entry.target.roles
                and big_city_member_role not in entry.target.roles
            ):
                await database.remove_member(discord_id=entry.target.id)
        elif (
            guardian_role in entry.before.roles
            and guardian_role not in entry.after.roles
        ):
            if (
                member_role not in entry.target.roles
                and deputy_role not in entry.target.roles
                and probation_role not in entry.target.roles
                and big_city_member_role not in entry.target.roles
            ):
                await database.remove_member(discord_id=entry.target.id)
        elif (
            big_city_member_role in entry.before.roles
            and big_city_member_role not in entry.after.roles
        ):
            if (
                member_role not in entry.target.roles
                and deputy_role not in entry.target.roles
                and guardian_role not in entry.target.roles
                and probation_role not in entry.target.roles
            ):
                await database.remove_member(discord_id=entry.target.id)


def setup(bot: commands.bot):
    bot.add_cog(Roles(bot))
    logger.info(f">{__name__} is launched")