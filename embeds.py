import disnake
from typing import Union


def build_embed(
    description: str,
    failure: bool = False,
    without_title: bool = False,
    color: Union[disnake.Color, int] = None,
) -> disnake.Embed:
    embed = disnake.Embed(
        title="ОШИБКА" if failure else "УСПЕХ",
        description=description,
        color=disnake.Color.red() if failure else disnake.Color.green(),
    )
    if without_title:
        embed.title = None
    if color is not None:
        embed.colour = color
    return embed