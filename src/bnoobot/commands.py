import os
import random
from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands import Context

from src.bnoobot.spotify import SpotifyHandler

from src.bnoobot.config_loader import ConfigLoader

# Use __file__ to get the path of main.py and determine its directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize logging and config
config_loader = ConfigLoader(script_dir)
config = config_loader.get_config()
logger = config_loader.get_logger()


@commands.command()
async def ping(ctx: Context) -> None:
    """Responds with 'Pong!' to test bot responsiveness.

    Args:
        ctx (Context): The context in which the command was invoked.
    """
    await ctx.send('Pong!')
    logger.info(f'{ctx.author} used the ping command in {ctx.guild.name}')


@commands.command()
async def hello(ctx: Context) -> None:
    """Responds with a greeting message.

    Args:
        ctx (Context): The context in which the command was invoked.
    """
    await ctx.send(f'Hello, {ctx.author}.')
    logger.info(f'{ctx.author} used the hello command in {ctx.guild.name}')


@commands.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx: Context, member: discord.Member, *, reason: Optional[str] = None) -> None:
    """Kicks a member from the server.

    Args:
        ctx (Context): The context in which the command was invoked.
        member (discord.Member): The member to kick.
        reason (Optional[str], optional): The reason for kicking the member. Defaults to None.
    """
    reason = reason or "No reason provided"
    await member.kick(reason=reason)
    await ctx.send(f'{member.name} has been kicked for: {reason}')
    logger.info(f'{ctx.author} used the kick command in {ctx.guild.name}')


@commands.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx: Context, member: discord.Member, *, reason: Optional[str] = None) -> None:
    """Bans a member from the server.

    Args:
        ctx (Context): The context in which the command was invoked.
        member (discord.Member): The member to ban.
        reason (Optional[str], optional): The reason for banning the member. Defaults to None.
    """
    reason = reason or "No reason provided"
    await member.ban(reason=reason)
    await ctx.send(f'{member.name} has been banned for: {reason}')
    logger.info(f'{ctx.author} used the ban command in {ctx.guild.name}')


@commands.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx: Context, *, user: str) -> None:
    """Unbans a previously banned user.

    Args:
        ctx (Context): The context in which the command was invoked.
        user (str): The username and discriminator of the user to unban, formatted as "username#discriminator".
    """
    banned_users = await ctx.guild.bans()
    username, discriminator = user.split('#')

    for ban_entry in banned_users:
        banned_user = ban_entry.user
        if banned_user.name == username and banned_user.discriminator == discriminator:
            await ctx.guild.unban(banned_user)
            await ctx.send(f'{banned_user.name} has been unbanned.')
            logger.info(f'{ctx.author} used the unban command in {ctx.guild.name} to unban {banned_user.name}')
            return
    await ctx.send(f'User {user} not found.')
    logger.info(f'{ctx.author} used the unban command in {ctx.guild.name} on an unrecognized user {user}')


@commands.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx: Context, member: discord.Member, *, reason: Optional[str] = None) -> None:
    """Mutes a member by adding the 'Muted' role.

    Args:
        ctx (Context): The context in which the command was invoked.
        member (discord.Member): The member to mute.
        reason (Optional[str], optional): The reason for muting the member. Defaults to None.
    """
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, speak=False, send_messages=False)
    await member.add_roles(role, reason=reason)
    await ctx.send(f'{member.mention} has been muted for: {reason}')
    logger.info(f'{ctx.author} used the mute command in {ctx.guild.name} on {member.mention} for reason: {reason}')


@commands.command()
async def poll(ctx: Context, *, question: str) -> None:
    """Creates a poll with thumbs up and thumbs down reactions.

    Args:
        ctx (Context): The context in which the command was invoked.
        question (str): The question to be polled.
    """
    message = await ctx.send(f'📊 Poll: {question}')
    await message.add_reaction('👍')
    await message.add_reaction('👎')


@commands.command(aliases=['8ball', 'eightball'])
async def _8ball(ctx: Context, *, question: str) -> None:
    """Answers a question using the magic 8-ball.

    Args:
        ctx (Context): The context in which the command was invoked.
        question (str): The question to ask the 8-ball.
    """
    responses = [
        "Yes, definitely.",
        "No, absolutely not.",
        "Maybe.",
        "Ask again later.",
        "It is certain.",
        "Very doubtful."
    ]
    answer = random.choice(responses)
    await ctx.send(f'Question: {question}\nAnswer: {answer}')
    logger.info(f'{ctx.author} used the 8ball command in {ctx.guild.name}. Question: {question} \nAnswer: {answer}')


@commands.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx: Context, amount: int = 5) -> None:
    """Clears a specified number of messages from the channel.

    Args:
        ctx (Context): The context in which the command was invoked.
        amount (int, optional): The number of messages to clear. Defaults to 5.
    """
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Deleted {amount} messages.', delete_after=5)
    logger.info(f'{ctx.author} used the clear command in {ctx.guild.name} and deleted {amount} messages.')


@commands.command()
async def schedule(ctx: Context, event_name: str, delay_minutes: int, description: Optional[str] = None) -> None:
    """Schedules a new event.

    Args:
        ctx (Context): The context in which the command was invoked.
        event_name (str): The name of the event.
        delay_minutes (int): The delay in minutes before the event triggers.
        description (Optional[str], optional): A description of the event. Defaults to None.
    """
    scheduler = ctx.bot.scheduler  # Access scheduler from the bot instance
    channel = ctx.channel
    await scheduler.schedule_event(event_name, channel, delay_minutes, description)


@commands.command()
async def list_events(ctx: Context) -> None:
    """Lists all scheduled events.

    Args:
        ctx (Context): The context in which the command was invoked.
    """
    scheduler = ctx.bot.scheduler  # Access scheduler from the bot instance
    events = await scheduler.list_scheduled_events()  # Fix: Await the coroutine
    if not events:
        await ctx.send("No events are currently scheduled.")
    else:
        for event in events:
            await ctx.send(f"Event: {event.event_name}, Scheduled for: {event.trigger_time}")


@commands.command()
async def remove_event(ctx: Context, event_name: str) -> None:
    """Removes a scheduled event by name.

    Args:
        ctx (Context): The context in which the command was invoked.
        event_name (str): The name of the event to remove.
    """
    scheduler = ctx.bot.scheduler  # Access scheduler from the bot instance
    if await scheduler.remove_event(event_name):  # Ensure this line checks if the event was removed
        await ctx.send(f"Event '{event_name}' has been removed from the schedule.")
    else:
        await ctx.send(f"Event '{event_name}' not found.")  # Send this if the event was not found


@commands.command()
async def help_schedule(ctx: Context) -> None:
    """Shows common time conversions for scheduling events.

    Args:
        ctx (Context): The context in which the command was invoked.
    """
    conversions = [
        ("One Hour", "60 Min"),
        ("Three Hours", "180 Min"),
        ("One Day", "1440 Min"),
        ("Two Days", "2880 Min"),
        ("Three Days", "4320 Min"),
        ("One Week", "10080 Min")
    ]

    message = "\n".join([f"{c[0]} is equal to: {c[1]}" for c in conversions])
    await ctx.send(message)


# Create an instance of the Spotify handler for spotify related commands to use to interact with the API
spotify_handler = SpotifyHandler(config['SPOTIFY_CLIENT_ID'], config['SPOTIFY_CLIENT_SECRET'])

# Command for fetching the top 25 Drum and Bass tracks
@commands.command(name='topdnb')
async def topdnb(ctx):
    # Inform the user that you're fetching the top tracks
    await ctx.send("Fetching top 25 Drum and Bass tracks...")

    # Fetch the top 25 drum and bass songs
    top_tracks = spotify_handler.get_top_drum_and_bass_tracks()

    # Send the list to the Discord channel
    for track in top_tracks:
        await ctx.send(track)


# Command for fetching the top 25 Drum and Bass tracks
@commands.command(name='topdub')
async def topdub(ctx):
    # Inform the user that you're fetching the top tracks
    await ctx.send("Fetching top 25 Dubstep tracks...")

    # Fetch the top 25 dubstep songs
    top_tracks = spotify_handler.get_top_dubstep_tracks()

    # Send the list to the Discord channel
    for track in top_tracks:
        await ctx.send(track)

# Command for fetching the top 25 Drum and Bass tracks
@commands.command(name='tophouse')
async def tophouse(ctx):
    # Inform the user that you're fetching the top tracks
    await ctx.send("Fetching top 25 House tracks...")

    # Fetch the top 25 drum and bass songs
    top_tracks = spotify_handler.get_top_house_tracks()

    # Send the list to the Discord channel
    for track in top_tracks:
        await ctx.send(track)