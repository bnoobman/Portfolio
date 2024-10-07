import discord
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
from discord.ext.commands import Context
from src.bnoobot.config_loader import ConfigLoader
from src.bnoobot.tasks import Tasks
from src.bnoobot.scheduler import Scheduler
from src.bnoobot.commands import (
    ping, hello, kick, ban, unban, mute, poll, _8ball, clear,
    help_schedule, schedule, list_events, remove_event
)


@pytest.fixture
def bot():
    """Fixture to create a bot instance."""
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.scheduler = MagicMock(spec=Scheduler)
    return bot


@pytest.fixture
def mock_context():
    """Fixture to create a mock context for testing commands."""
    ctx = MagicMock(spec=Context)
    ctx.send = AsyncMock()
    ctx.author = MagicMock()
    ctx.message = MagicMock()
    ctx.command = MagicMock()  # Add this to mock the command attribute
    return ctx


@pytest.fixture
def tasks_instance(bot):
    """Fixture to create a mock Tasks instance."""
    config = {"DISCORD_TOKEN": "test_token"}
    logger = MagicMock()
    tasks = Tasks(bot, config, logger)
    tasks.start_tasks = AsyncMock()
    return tasks


def test_command_registration(bot):
    """Test if commands are registered correctly."""

    # Register commands explicitly in the test
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

    # Check if specific commands are registered
    command_names = bot.commands.keys()

    assert 'ping' in command_names
    assert 'hello' in command_names
    assert 'kick' in command_names
    assert 'ban' in command_names
    assert 'unban' in command_names
    assert 'mute' in command_names
    assert 'poll' in command_names
    assert '8ball' in command_names
    assert 'clear' in command_names
    assert 'schedule' in command_names
    assert 'list_events' in command_names
    assert 'remove_event' in command_names
    assert 'help_schedule' in command_names


@patch('src.bnoobot.config_loader.ConfigLoader.get_logger', return_value=MagicMock())
async def test_on_ready(tasks_instance, bot, mock_logger):
    bot.user = MagicMock(name="TestBot")

    # Mock the logger and tasks
    tasks_instance.start_tasks = AsyncMock()

    # Call the on_ready event handler
    await bot.dispatch('ready')

    # Verify the logger and task start
    mock_logger().info.assert_called_once_with(f'Bot has logged in as {bot.user}')
    tasks_instance.start_tasks.assert_called_once()


@pytest.mark.asyncio
async def test_on_command_error_command_not_found(mock_context, bot):
    """Test the on_command_error event with CommandNotFound."""
    error = commands.CommandNotFound()
    bot.dispatch = AsyncMock()
    await bot.on_command_error(mock_context, error)

    mock_context.send.assert_called_once_with(f'What the heck do you mean by, "{mock_context.message.content}"?!')


@pytest.mark.asyncio
async def test_on_command_error_missing_permissions(mock_context, bot):
    """Test the on_command_error event with MissingPermissions."""
    error = commands.MissingPermissions(['kick_members'])
    await bot.on_command_error(mock_context, error)

    mock_context.send.assert_called_once_with(f'Sorry, you don’t have permission to do that.')


@pytest.mark.asyncio
async def test_on_command_error_generic(mock_context, bot):
    """Test the on_command_error event with a generic error."""
    error = commands.CommandInvokeError(Exception('Test error'))
    await bot.on_command_error(mock_context, error)

    mock_context.send.assert_called_once_with(f'An error occurred: Test error')


@pytest.mark.asyncio
async def test_tasks_start_called_on_ready(tasks_instance, bot):
    """Test if Tasks.start_tasks is called when the bot is ready."""

    # Patch bot.user to mock its value
    with patch.object(bot, 'user', new=MagicMock(name="TestBot")):
        # Simulate on_ready event
        await bot.dispatch('ready')

        # Ensure that the start_tasks method was called
        tasks_instance.start_tasks.assert_called_once()

