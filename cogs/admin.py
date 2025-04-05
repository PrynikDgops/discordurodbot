import disnake
from disnake.ext import commands
from utils.config import load_config, save_config

def allowed_check(inter: disnake.ApplicationCommandInteraction) -> bool:
    """Check if the user has access to the commands."""
    allowed_users = config.get("command_access_users", [])
    allowed_roles = config.get("command_access_roles", [])
    member = inter.author

    # Check if the user is in the allowed users list
    if member.id in allowed_users:
        return True

    # Check if the user has any of the allowed roles
    for role in member.roles:
        if role.id in allowed_roles:
            return True

    return False

config = load_config()

class AdminCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="выдать-доступ-пользователю", description="Выдает доступ к командам указанному пользователю.")
    @commands.check(allowed_check) # type: ignore
    async def grant_access_user(inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        allowed_users = config.get("command_access_users", [])
        if member.id not in allowed_users:
            allowed_users.append(member.id)
            config["command_access_users"] = allowed_users
            save_config(config)
            await inter.response.send_message(f"{member.mention} теперь имеет доступ к командам.", ephemeral=True)
        else:
            await inter.response.send_message(f"{member.mention} уже имеет доступ.", ephemeral=True)


    @commands.slash_command(name="отозвать-доступ-пользователя", description="Отзывает доступ к командам у указанного пользователя.")
    @commands.check(allowed_check)
    async def revoke_access_user(inter: disnake.ApplicationCommandInteraction, member: disnake.Member):
        allowed_users = config.get("command_access_users", [])
        if member.id in allowed_users:
            allowed_users.remove(member.id)
            config["command_access_users"] = allowed_users
            save_config(config)
            await inter.response.send_message(f"Доступ для {member.mention} отозван.", ephemeral=True)
        else:
            await inter.response.send_message(f"{member.mention} не имеет доступа.", ephemeral=True)


    @commands.slash_command(name="список-доверенных-пользователей", description="Выводит список пользователей, имеющих доступ к командам.")
    @commands.check(allowed_check)
    async def list_access_users(inter: disnake.ApplicationCommandInteraction):
        allowed_users = config.get("command_access_users", [])
        if not allowed_users:
            await inter.response.send_message("Список доверенных пользователей пуст.", ephemeral=True)
            return
        users = []
        for user_id in allowed_users:
            member = inter.guild.get_member(user_id)
            if member:
                users.append(member.mention)
            else:
                users.append(str(user_id))
        await inter.response.send_message("Доверенные пользователи: " + ", ".join(users), ephemeral=True)


    @commands.slash_command(name="выдать-доступ-роли", description="Выдает доступ к командам указанной роли.")
    @commands.check(allowed_check)
    async def grant_access_role(inter: disnake.ApplicationCommandInteraction, role: disnake.Role):
        allowed_roles = config.get("command_access_roles", [])
        if role.id not in allowed_roles:
            allowed_roles.append(role.id)
            config["command_access_roles"] = allowed_roles
            save_config(config)
            await inter.response.send_message(f"Роль {role.name} теперь имеет доступ к командам.", ephemeral=True)
        else:
            await inter.response.send_message(f"Роль {role.name} уже имеет доступ.", ephemeral=True)


    @commands.slash_command(name="отозвать-доступ-роли", description="Отзывает доступ к командам у указанной роли.")
    @commands.check(allowed_check)
    async def revoke_access_role(inter: disnake.ApplicationCommandInteraction, role: disnake.Role):
        allowed_roles = config.get("command_access_roles", [])
        if role.id in allowed_roles:
            allowed_roles.remove(role.id)
            config["command_access_roles"] = allowed_roles
            save_config(config)
            await inter.response.send_message(f"Доступ для роли {role.name} отозван.", ephemeral=True)
        else:
            await inter.response.send_message(f"Роль {role.name} не имеет доступа.", ephemeral=True)


    @commands.slash_command(name="список-доверенных-ролей", description="Выводит список ролей, имеющих доступ к командам.")
    @commands.check(allowed_check)
    async def list_access_roles(inter: disnake.ApplicationCommandInteraction):
        allowed_roles = config.get("command_access_roles", [])
        if not allowed_roles:
            await inter.response.send_message("Список доверенных ролей пуст.", ephemeral=True)
            return
        roles = []
        for role_id in allowed_roles:
            role = inter.guild.get_role(role_id)
            if role:
                roles.append(role.name)
            else:
                roles.append(str(role_id))
        await inter.response.send_message("Доверенные роли: " + ", ".join(roles), ephemeral=True)
        pass

def setup(bot: commands.Bot):
    bot.add_cog(AdminCommands(bot))