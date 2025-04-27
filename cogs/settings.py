import disnake
from disnake.ext import commands
from utils.helpers import allowed_check
from utils.config import load_config, save_config

config = load_config()

class SettingsCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="добавить-применяемую-роль", description="Добавляет роль в список применимых ролей.")
    @commands.check(allowed_check)
    async def add_applicable_role(inter: disnake.ApplicationCommandInteraction, role: disnake.Role):
        applicable = config.get("applicable_roles", [])
        if role.id not in applicable:
            applicable.append(role.id)
            config["applicable_roles"] = applicable
            save_config(config)
            await inter.response.send_message(f"Роль {role.name} добавлена в список применимых ролей.", ephemeral=True)
        else:
            await inter.response.send_message(f"Роль {role.name} уже присутствует.", ephemeral=True)

    @commands.slash_command(name="удалить-применяемую-роль", description="Удаляет роль из списка применимых ролей.",)
    @commands.check(allowed_check)
    async def remove_applicable_role(inter: disnake.ApplicationCommandInteraction, role: disnake.Role):
        applicable = config.get("applicable_roles", [])
        if role.id in applicable:
            applicable.remove(role.id)
            config["applicable_roles"] = applicable
            save_config(config)
            await inter.response.send_message(f"Роль {role.name} удалена из списка применимых ролей.", ephemeral=True)
        else:
            await inter.response.send_message(f"Роль {role.name} не найдена.", ephemeral=True)


    @commands.slash_command(name="список-применимых-ролей", description="Выводит список применимых ролей.")
    @commands.check(allowed_check)
    async def applicable_roles_list(inter: disnake.ApplicationCommandInteraction):
        applicable = config.get("applicable_roles", [])
        if not applicable:
            await inter.response.send_message("Список применимых ролей пуст (применяются все участники).", ephemeral=True)
            return
        roles_names = []
        for role_id in applicable:
            role = inter.guild.get_role(role_id)
            if role:
                roles_names.append(role.name)
            else:
                roles_names.append(str(role_id))
        await inter.response.send_message("Применимые роли: " + ", ".join(roles_names), ephemeral=True)

    @commands.slash_command(name="установить-время-работы", description="Устанавливает требуемое время работы (часы).",)
    async def set_required_work_time(inter: disnake.ApplicationCommandInteraction, hours: float):
        config["required_work_time_hours"] = hours
        save_config(config)
        await inter.response.send_message(f"Требуемое время работы установлено: {hours} часов.", ephemeral=True)
        
    @commands.slash_command(name="установить-период-работы", description="Устанавливает период проверки отчетности (часы).",)
    @commands.check(allowed_check)
    async def set_report_check_period(
        inter: disnake.ApplicationCommandInteraction, hours: float):
        config["report_check_period_hours"] = hours
        save_config(config)
        await inter.response.send_message(f"Период проверки отчетности установлен: {hours} часов.", ephemeral=True)
        pass

def setup(bot: commands.Bot):
    bot.add_cog(SettingsCommands(bot))