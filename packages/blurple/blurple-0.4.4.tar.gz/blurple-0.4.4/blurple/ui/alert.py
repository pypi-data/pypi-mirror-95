from .style import Style
import discord


class Alert(discord.Embed):
    """ A subclass of :class:`discord.Embed` for stylish alert messages.

        :param Style style: The style of the alert.
        :param str title: The title of the alert, will be wrapped in emoji and alert name unless specified in options.
        :param str description: An optional description of the alert, use your imagination for it's use.
        :param **options: Alert options to customize it's look.

            :emoji: Defaults to :class:`True`. Can be set to false to remove the emoji from the alert title.
            :name: Defaults to :class:`True`. Can be set to false to remove the name of the alert from the title.
    """

    def __init__(self, style: Style, title: str, description: str = discord.Embed.Empty, **options):
        super().__init__(
            color=style[0],
            title=self.process_title(style, title, **options),
            description=description
        )

    @classmethod
    def process_title(cls, style: Style, title: str, **options):
        output: str = ''

        if options.get("emoji") is not False:
            output += style[1] + " "

        if (name := options.get("name", style[2])) is not False:
            output += f"`{name}:` "

        return output + f"**{title}**"
