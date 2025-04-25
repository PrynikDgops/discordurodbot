import disnake
from disnake.ext import commands
from disnake import VoiceChannel, StageChannel, ApplicationCommandInteraction
from typing import Optional, Union
from utils.config import load_config
from utils.helpers import allowed_check, is_applicable

bot = commands.InteractionBot()  # Define the bot instance

config = load_config()

class VoiseCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @bot.slash_command(
        name="пропинговка",
        description="Упоминает пользователей, не находящихся в голосовом/Stage канале.",
    )
    @commands.check(allowed_check)
    async def mention_not_in_channel(
        inter: disnake.ApplicationCommandInteraction,
        channel: Optional[Union[disnake.VoiceChannel, disnake.StageChannel]] = None,
    ):
        await inter.response.defer()
        if channel:
            not_in_channel = [
                member.mention
                for member in inter.guild.members
                if (member.voice is None or member.voice.channel != channel)
                and not member.bot
                and member.id not in config.get("whitelist", [])
                and is_applicable(member)
            ]
        else:
            not_in_channel = [
                member.mention
                for member in inter.guild.members
                if member.voice is None
                and not member.bot
                and member.id not in config.get("whitelist", [])
                and is_applicable(member)
            ]
        if not not_in_channel:
            await inter.response.send_message(
                "Все подходящие пользователи находятся в голосовых каналах!", ephemeral=True
            )
            return
        messages = []
        msg_chunk = ""
        for mention in not_in_channel:
            if len(msg_chunk) + len(mention) + 1 > 1900:
                messages.append(msg_chunk)
                msg_chunk = mention + " "
            else:
                msg_chunk += mention + " "
        if msg_chunk:
            messages.append(msg_chunk)
        for msg in messages:
            await inter.followup.send(msg)

def setup(bot: commands.Bot):
    bot.add_cog(VoiseCommands(bot))