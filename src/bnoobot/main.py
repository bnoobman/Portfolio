import os

import discord
from discord.ext import commands
from discord.ext.commands import Context

from src.bnoobot.commands import (
    ping, hello, kick, ban, unban, mute, poll, _8ball, clear,
    help_schedule, schedule, list_events, remove_event, topdnb,
    topdub, tophouse
)
from src.bnoobot.config_loader import ConfigLoader
from src.bnoobot.scheduler import Scheduler
from src.bnoobot.tasks import Tasks
from src.bnoobot.chess_checker import setup_chess_checker

# Use __file__ to get the path of main.py and determine its directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize logging and config
config_loader = ConfigLoader(script_dir)
config = config_loader.get_config()
logger = config_loader.get_logger()

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Attach scheduler to the bot instance so that commands can access it
bot.scheduler = Scheduler(bot, logger)

# Initialize tasks
tasks = Tasks(bot, config, logger)

# Register bot commands
bot.add_command(ping)
bot.add_command(hello)
bot.add_command(kick)
bot.add_command(ban)
bot.add_command(unban)
bot.add_command(mute)
bot.add_command(poll)
bot.add_command(_8ball)
bot.add_command(clear)
bot.add_command(schedule)
bot.add_command(list_events)
bot.add_command(remove_event)
bot.add_command(help_schedule)
bot.add_command(topdnb)
bot.add_command(topdub)
bot.add_command(tophouse)


@bot.event
async def on_ready() -> None:
    """Event handler called when the bot has successfully connected to Discord.

    Logs the bot's login and starts scheduled tasks.
    """
    logger.info(f'Bot has logged in as {bot.user}')
    tasks.start_tasks()
    await setup_chess_checker(bot, config['DISCORD_CHANNEL_ID'])

@bot.event
async def on_command_error(ctx: Context, error: commands.CommandError) -> None:
    """Event handler for handling command errors.

    Args:
        ctx (Context): The context in which the error occurred.
        error (commands.CommandError): The command error that occurred.
    """
    if isinstance(error, commands.CommandNotFound):
        logger.warning(f'{ctx.author} tried to use an unknown command: {ctx.message.content}')
        await ctx.send(f'What the heck do you mean by, "{ctx.message.content}"?!')
    elif isinstance(error, commands.MissingPermissions):
        logger.warning(f'{ctx.author} tried to use a command without proper permissions.')
        await ctx.send(f'Sorry, you don’t have permission to do that.')
    else:
        logger.error(f'An error occurred: {str(error)}')
        await ctx.send(f'An error occurred: {str(error)}')


if __name__ == '__main__':
    bot.run(config['DISCORD_TOKEN'])
