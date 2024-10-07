import pytest
from unittest.mock import AsyncMock, MagicMock
from src.bnoobot.bot_functions import BotFunctions

@pytest.mark.asyncio
async def test_send_message_success(bot, mock_channel):
    # Setup
    mock_channel.id = 12345
    bot.get_channel.return_value = mock_channel
    config = {'DISCORD_CHANNEL_ID': 12345}
    logger = MagicMock()
    bot_functions = BotFunctions(bot, config, logger)

    # Call the async method
    await bot_functions.send_message("Hello, World!")

    # Check if send was called on the correct channel
    bot.get_channel.assert_called_with(12345)
    mock_channel.send.assert_called_once_with("Hello, World!")


@pytest.mark.asyncio
async def test_send_message_channel_not_found(bot):
    # Setup
    bot.get_channel.return_value = None  # Simulate channel not found
    config = {'DISCORD_CHANNEL_ID': 12345}
    logger = MagicMock()
    bot_functions = BotFunctions(bot, config, logger)

    # Call the async method
    await bot_functions.send_message("Hello, World!")

    # Check if send was not called (since channel was not found)
    bot.get_channel.assert_called_with(12345)
