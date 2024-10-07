import sys
import os

# Add "src" directory to sys.path to resolve imports from "src.bnoobot"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


import pytest
from unittest.mock import AsyncMock, MagicMock
from discord.ext import commands
import discord

@pytest.fixture
def bot():
    intents = discord.Intents.default()
    intents.message_content = True  # Enable message content intent if required by your bot
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.get_channel = MagicMock()
    return bot

@pytest.fixture
def mock_channel():
    mock_channel = MagicMock()
    mock_channel.send = AsyncMock()
    return mock_channel

@pytest.fixture
def mock_context(mock_channel):
    ctx = MagicMock()
    ctx.guild = MagicMock()
    ctx.author = MagicMock()
    ctx.send = AsyncMock()
    ctx.channel = mock_channel
    return ctx
