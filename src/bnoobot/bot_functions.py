class BotFunctions:
    """A class for managing bot-related functions such as sending messages to a Discord channel.

    Args:
        bot (discord.ext.commands.Bot): The Discord bot instance.
        config (dict): The bot's configuration data, including the Discord channel ID.
        logger (logging.Logger): Logger instance for logging events.
    """

    def __init__(self, bot, config: dict, logger) -> None:
        """Initializes the BotFunctions class with the bot, config, and logger.

        Args:
            bot (discord.ext.commands.Bot): The Discord bot instance.
            config (dict): Configuration data loaded from a file.
            logger (logging.Logger): Logger instance for logging events.
        """
        self.bot = bot
        self.config = config
        self.logger = logger

    async def send_message(self, content: str) -> None:
        """Sends a message to a specific Discord channel.

        Args:
            content (str): The message content to send to the specified channel.
        """
        channel = self.bot.get_channel(self.config['DISCORD_CHANNEL_ID'])
        if channel:
            await channel.send(content)
        else:
            print("Channel not found. Check your channel ID and try again.")
