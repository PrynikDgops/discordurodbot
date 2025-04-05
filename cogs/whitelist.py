from discord.ext.commands import bot
import disnake # type: ignore
from disnake.ext import commands # type: ignore
from utils.config import load_config, save_config

config = load_config()

class WhitelistCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="добавить-в-вайтлист", description="Добавляет пользователя в whitelist.")
    async def whitelist_add(inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        whitelist_list = config.get("whitelist", [])
        if member.id not in whitelist_list:
            whitelist_list.append(member.id)
            config["whitelist"] = whitelist_list
            save_config(config)
            await inter.response.send_message(
                f"{member.display_name} добавлен в whitelist.", ephemeral=True)
        else:
            await inter.response.send_message(
            f"{member.display_name} уже в whitelist.", ephemeral=True)


    @commands.slash_command(name="убрать-из-вайтлиста", description="Удаляет пользователя из whitelist.")
    @commands.check(allowed_check) # type: ignore
    async def whitelist_remove_cmd(
        inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        whitelist_list = config.get("whitelist", [])
        if member.id in whitelist_list:
            whitelist_list.remove(member.id)
            config["whitelist"] = whitelist_list
            save_config(config)
            await inter.response.send_message(
                f"{member.display_name} удалён из whitelist.", ephemeral=True)
        else:
            await inter.response.send_message(
                f"{member.display_name} не найден в whitelist.", ephemeral=True)


    @commands.slash_command(name="список-вайтлиста", description="Выводит список пользователей в whitelist.")
    @commands.check(allowed_check) # type: ignore
    async def whitelist_list_cmd(inter: disnake.ApplicationCommandInteraction):
        whitelist_list = config.get("whitelist", [])
        if not whitelist_list:
            await inter.response.send_message("Whitelist пуст.", ephemeral=True)
            return
        members_list = []
        for user_id in whitelist_list:
            member = inter.guild.get_member(user_id)
            if member:
                members_list.append(member.mention)
            else:
                members_list.append(str(user_id))
        await inter.response.send_message(
            "Whitelist: " + ", ".join(members_list), ephemeral=True)

        pass

def setup(bot: commands.Bot):
    bot.add_cog(WhitelistCommands(bot))