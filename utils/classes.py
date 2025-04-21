import logging

import disnake
from disnake.ext import commands
from typing import Optional

from utils import config, database

logger = logging.getLogger(__name__)


class BotConfig:
    def __init__(
        self,
        main_guild_id: int,
        city_member_role_id: int,
        probation_role_id: int,
        report_channel_id: int,
        log_channel_id: int,
        owner_id: int,
        deputy_role_id: int,
        guardian_role_id: int,
        big_city_member_role_id: int,
        members_count_channel_id: int,
        head_role_id: int,
    ):
        self.main_guild_id = main_guild_id
        self.city_member_role_id = city_member_role_id
        self.probation_role_id = probation_role_id
        self.report_channel_id = report_channel_id
        self.log_channel_id = log_channel_id
        self.owner_id = owner_id
        self.deputy_role_id = deputy_role_id
        self.guardian_role_id = guardian_role_id
        self.big_city_member_role_id = big_city_member_role_id
        self.members_count_channel_id = members_count_channel_id
        self.head_role_id = head_role_id

    async def get_main_guild(self, bot: commands.Bot) -> disnake.Guild:
        return bot.get_guild(self.main_guild_id)

    async def update_config_data(self, **kwargs):
        await config.update_config_data(bot_config=self, **kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    async def get_city_member_role(self, bot: commands.Bot) -> Optional[disnake.Role]:
        main_guild = await self.get_main_guild(bot)
        if main_guild is None:
            return None

        role = main_guild.get_role(self.city_member_role_id)

        return role

    async def get_probation_role(self, bot: commands.Bot) -> Optional[disnake.Role]:
        main_guild = await self.get_main_guild(bot)
        if main_guild is None:
            return None

        role = main_guild.get_role(self.probation_role_id)

        return role

    async def get_deputy_role(self, bot: commands.Bot) -> Optional[disnake.Role]:
        main_guild = await self.get_main_guild(bot)
        if main_guild is None:
            return None

        role = main_guild.get_role(self.deputy_role_id)

        return role

    async def get_head_role(self, bot: commands.Bot) -> Optional[disnake.Role]:
        main_guild = await self.get_main_guild(bot)
        if main_guild is None:
            return None

        role = main_guild.get_role(self.head_role_id)

        return role

    async def get_guardian_role(self, bot: commands.Bot) -> Optional[disnake.Role]:
        main_guild = await self.get_main_guild(bot)
        if main_guild is None:
            return None

        role = main_guild.get_role(self.guardian_role_id)

        return role

    async def get_big_city_member_role(
        self, bot: commands.Bot
    ) -> Optional[disnake.Role]:
        main_guild = await self.get_main_guild(bot)
        if main_guild is None:
            return None

        role = main_guild.get_role(self.big_city_member_role_id)

        return role

    async def get_report_channel(
        self, bot: commands.Bot
    ) -> Optional[disnake.TextChannel]:
        main_guild = await self.get_main_guild(bot)
        if main_guild is None:
            return None

        channel = main_guild.get_channel(self.report_channel_id)
        return channel

    async def get_log_channel(self, bot: commands.Bot) -> Optional[disnake.TextChannel]:
        main_guild = await self.get_main_guild(bot)
        if main_guild is None:
            return None

        channel = main_guild.get_channel(self.log_channel_id)
        return channel

    async def get_owner(self, bot: commands.Bot) -> Optional[disnake.User]:
        return await bot.fetch_user(self.owner_id)

    async def update_member_count_channel_name(self, bot: commands.Bot) -> Optional[str]:
        members_count = len(await database.get_all_users())
        main_guild = await self.get_main_guild(bot)
        if main_guild is None:
            return None

        channel = main_guild.get_channel(self.members_count_channel_id)

        name = "👥 Население: " + str(members_count)

        await channel.edit(name=name)
        return name