import logging
import disnake
from disnake.ext import commands, tasks

import settings
from utils import sync_functions

logger = logging.getLogger()

owner = [302065849722732544]


class UrodCityPointer(commands.Bot):
    @classmethod
    def create(cls) -> "UrodCityPointer":
        return cls(
            owner_ids=set(owner),
            status=disnake.Status.online,
            intents=disnake.Intents.all(),
            command_prefix=None,
            allowed_mentions=disnake.AllowedMentions(),
            activity=disnake.Activity(
                type=disnake.ActivityType.watching, name="больше не за поинтами"
            ),
            description="больше не считает поинты города уродов",
        )

    async def on_ready(self):
        logger.info(f"Logged in as {self.user.name}")
        self.sync_database.start()
        self.sync_report.start()

    @tasks.loop(hours=1)
    async def sync_database(self):
        await sync_functions.setup_database(bot=self)
        await settings.BOT_CONFIG.update_member_count_channel_name(bot=self)

    @tasks.loop(seconds=55)
    async def sync_report(self):
        await sync_functions.report_sync(bot=self)