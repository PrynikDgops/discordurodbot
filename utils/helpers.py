from disnake import Member
import disnake
from disnake.ext.commands import Context
from datetime import datetime, timedelta
import re
from utils.config import load_config

config = load_config()
whitelist = config.get("whitelist", [])

def is_applicable(member: disnake.Member) -> bool:
    """Возвращает True, если список applicable_roles пуст или участник имеет хотя бы одну из указанных ролей."""
    applicable_roles = config.get("applicable_roles", [])
    if not applicable_roles:
        return True
    return any(role.id in applicable_roles for role in member.roles)

async def allowed_check(ctx: Context) -> bool:
    """Проверяет, имеет ли пользователь доступ к командам."""
    if ctx.author.guild_permissions.administrator:
        return True
    allowed_users = config.get("command_access_users", [])
    allowed_roles = config.get("command_access_roles", [])
    if ctx.author.id in allowed_users:
        return True
    return any(role.id in allowed_roles for role in ctx.author.roles)
def is_applicable(member: Member) -> bool:
    applicable_roles = config.get("applicable_roles", [])
    return not applicable_roles or any(role.id in applicable_roles for role in member.roles)

async def generate_report(report_channel, period: float) -> str:
    now = datetime.now()
    after_time = now - timedelta(hours=period)
    messages = await report_channel.history(after=after_time).flatten()
    work_times = {}
    pattern = r"(\d+(?:[.,]\d+)?)"
    for msg in messages:
        match = re.search(pattern, msg.content)
        if match:
            hours_str = match.group(1).replace(",", ".")
            try:
                hours_val = float(hours_str)
                work_times[msg.author.id] = work_times.get(msg.author.id, 0) + hours_val
                await msg.add_reaction("✅")
            except Exception:
                await msg.add_reaction("❌")
        else:
            await msg.add_reaction("❌")
    required_minutes = config["required_work_time_hours"] * 60
    worked_enough = []
    worked_insufficient = []
    not_worked = []
    for member in report_channel.guild.members:
        if member.bot or not is_applicable(member) or member.id in whitelist:
            continue
        total = work_times.get(member.id, 0)
        if total >= required_minutes:
            worked_enough.append(f"{member.mention} ({total:.0f} мин)")
        elif total > 0:
            worked_insufficient.append(f"{member.mention} ({total:.0f} мин)")
        else:
            not_worked.append(member.mention)
    report = (
        f"Отчетность за последние {period} часов\n\n"
        f"1. Работал достаточно (>= {config['required_work_time_hours']} ч):\n"
        + ("\n".join(worked_enough) if worked_enough else "Нет данных")
        + "\n\n"
        + f"2. Работал, но не достаточно (< {config['required_work_time_hours']} ч):\n"
        + ("\n".join(worked_insufficient) if worked_insufficient else "Нет данных")
        + "\n\n"
        + "3. Не работал:\n"
        + ("\n".join(not_worked) if not_worked else "Нет данных")
    )
    return report
    pass