import asyncio
import os
from datetime import datetime
from typing import List, Dict

import pytz
import requests
import yfinance as yf
from discord.ext import tasks
from discord.ext.commands import Bot

from .config_loader import ConfigLoader

# Use __file__ to get the path of main.py and determine its directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize logging and config
config_loader = ConfigLoader(script_dir)
config = config_loader.get_config()
logger = config_loader.get_logger()


class Tasks:
    """A class to manage periodic tasks for checking Twitch streamers and fetching stock prices.

    Args:
        bot (Bot): The Discord bot instance.
        config (Dict[str, Any]): The bot's configuration data.
        logger (logging.Logger): The logger for logging events.
    """

    def __init__(self, bot: Bot, config: Dict[str, any], logger) -> None:
        """Initializes the Tasks class.

        Args:
            bot (Bot): The Discord bot instance.
            config (Dict[str, Any]): Configuration data loaded from the YAML file.
            logger (logging.Logger): The logger instance for logging events.
        """
        self.bot = bot
        self.config = config
        self.logger = logger

    @staticmethod
    def get_twitch_oauth_token() -> str:
        """Gets OAuth token from Twitch API.

        Returns:
            str: The OAuth token for accessing the Twitch API.
        """
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": config['TWITCH_CLIENT_ID'],
            "client_secret": config['TWITCH_CLIENT_SECRET'],
            "grant_type": "client_credentials"
        }
        response = requests.post(url, params=params)
        response.raise_for_status()
        return response.json()["access_token"]

    @tasks.loop(minutes=15)
    async def check_streamers(self, token: str) -> None:
        """Checks if a Twitch streamer is live and sends a message to the Discord channel if they are.

        Args:
            token (str): The OAuth token for authentication with the Twitch API.
        """
        channel = self.bot.get_channel(config['DISCORD_CHANNEL_ID'])
        oauth_token = token

        for streamer in config['FAVORITE_STREAMERS']:
            try:
                if await self.is_streamer_live(streamer, oauth_token):
                    await channel.send(f"{streamer} is now live on Twitch!")
                else:
                    print(f"{streamer} is not live.")  # Print to STDOUT, don't blow up the log file
            except Exception as e:
                logger.error(f"Error checking {streamer}: {e}")

    @staticmethod
    async def is_streamer_live(streamer: str, oauth_token: str) -> bool:
        """Checks if a specific Twitch streamer is live.

        Args:
            streamer (str): The Twitch streamer username.
            oauth_token (str): OAuth token for authentication with the Twitch API.

        Returns:
            bool: True if the streamer is live, False otherwise.
        """
        url = "https://api.twitch.tv/helix/streams"
        headers = {
            "Client-ID": config['TWITCH_CLIENT_ID'],
            "Authorization": f"Bearer {oauth_token}"
        }
        params = {"user_login": streamer}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()["data"]
        return len(data) > 0  # If data is not empty, the streamer is live

    @tasks.loop(minutes=10)
    async def fetch_stock_prices(self):
        """Fetch the latest stock prices and send them to a Discord channel when the market is open."""
        while True:
            # Only fetch and send prices if the market is open
            if self.is_market_open():
                stock_prices = []
                for stock in config['STOCKS']:
                    stock_info = yf.Ticker(stock)
                    hist = stock_info.history(period="1d")

                    # Ensure there's enough data to calculate previous close
                    if len(hist) >= 2:
                        price = hist['Close'].iloc[-1]
                        prev_close = hist['Close'].iloc[-2]
                        percent_change = ((price - prev_close) / prev_close) * 100
                        stock_prices.append(
                            f"**{stock}**\nPrice: ${price:.2f}\nChange: {percent_change:.2f}%\n"
                        )
                    elif len(hist) == 1:
                        price = hist['Close'].iloc[-1]
                        stock_prices.append(
                            f"**{stock}**\nPrice: ${price:.2f}\n(No previous day data available)\n"
                        )
                    else:
                        stock_prices.append(f"**{stock}**\nNo data available\n")

                # Send the stock prices to the Discord channel
                channel = self.bot.get_channel(config['DISCORD_CHANNEL_ID'])
                if channel is not None:
                    await channel.send("**Stock Prices Update**:\n" + "\n".join(stock_prices))

            else:
                print("Market is closed. No updates at this time.")

            # Wait 15 minutes (900 seconds) before checking again
            await asyncio.sleep(900)

    @staticmethod
    def is_market_open() -> bool:
        """Checks if the stock market is currently open based on Eastern Time.

        Returns:
            bool: True if the market is open, False if it is closed.
        """
        tz = pytz.timezone('US/Eastern')
        current_time = datetime.now(tz)

        # Check if it's a weekday and within market hours
        if current_time.weekday() < 5:  # Monday to Friday
            if ((current_time.hour > config['STOCK_MARKET_OPEN'] or
                 (current_time.hour == config['STOCK_MARKET_OPEN'] and current_time.minute >= 30)) and
                    current_time.hour < config['STOCK_MARKET_CLOSE']):
                return True
        return False

    def start_tasks(self) -> None:
        """Starts the periodic tasks for checking streamers and fetching stock prices."""
        self.check_streamers.start(token=self.get_twitch_oauth_token())
        self.bot.loop.create_task(self.fetch_stock_prices())
