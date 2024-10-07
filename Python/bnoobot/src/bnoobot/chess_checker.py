import os

import discord
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.bnoobot.config_loader import ConfigLoader

# Use __file__ to get the path of main.py and determine its directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize logging and config
config_loader = ConfigLoader(script_dir)
config = config_loader.get_config()
logger = config_loader.get_logger()


class ChessGameChecker:
    def __init__(self, bot, discord_channel_id):
        self.bot = bot
        self.channel_id = discord_channel_id
        self.scheduler = AsyncIOScheduler()
        # I think I'm getting rate limited? Changing interval to 10 min... yay for testing...
        self.scheduler.add_job(self.check_games, "interval", minutes=10)
        self.scheduler.start()

    async def fetch_ongoing_games(self):
        """Fetches ongoing games from Chess.com for the specified username."""
        try:
            # todo figure out why the fuck importing this via config['CHESS_API_URL'] throws a fucking 403
            # but the hard coded fucking value of it throws a different error like it's not fucking disallowed at all...
            response = requests.get("https://api.chess.com/pub/player/bnoobman/games")
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            games = response.json().get("games", [])
            logger.info(f"Fetched {len(games)} games.")
            return games
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching games from Chess.com: {e}")
            return []  # Return an empty list if the request fails
        except ValueError as e:
            logger.error(f"Error parsing response from Chess.com: {e}")
            return []

    async def check_games(self):
        """Checks if it's your turn on any ongoing games and posts to Discord."""
        try:
            ongoing_games = await self.fetch_ongoing_games()

            if not ongoing_games:
                logger.info("No ongoing games found or an error occurred.")
                return

            for game in ongoing_games:
                if self.is_my_turn(game):
                    await self.post_to_discord(game)
        except Exception as e:
            logger.error(f"Error during game check: {e}")

    def is_my_turn(self, game):
        """Checks if it's your turn in the game."""
        try:
            # Get the current player's turn (white or black)
            current_turn = game["turn"]

            # Get the white and black player URLs and extract usernames from them
            white_player_url = game["white"]
            black_player_url = game["black"]

            white_username = white_player_url.split("/")[-1].lower()  # Extract and lowercase the username
            black_username = black_player_url.split("/")[-1].lower()

            my_username = config['CHESS_USERNAME'].lower()  # Make sure to compare in lowercase

            # Determine if it's your turn
            if current_turn == "white" and white_username == my_username:
                return True
            elif current_turn == "black" and black_username == my_username:
                return True

        except KeyError as e:
            logger.error(f"Error in game data format, missing key: {e}")
        return False

    async def post_to_discord(self, game):
        """Posts the game link to the specified Discord channel."""
        try:
            channel = self.bot.get_channel(self.channel_id)
            if channel is None:
                logger.error(f"Channel with ID {self.channel_id} not found.")
                return

            logger.info(f"Posting game {game['url']} to Discord channel {self.channel_id}.")

            # Send a message in the Discord channel
            await channel.send(f"It's your turn in a game: {game['url']}")
            logger.info(f"Successfully posted game link to Discord channel {self.channel_id}.")
        except discord.Forbidden:
            logger.error(f"Bot doesn't have permission to post in channel {self.channel_id}.")
        except discord.HTTPException as e:
            logger.error(f"Error sending message to Discord: {e}")
        except KeyError as e:
            logger.error(f"Game data missing required URL key: {e}")

# To use in your main bot
async def setup_chess_checker(bot, discord_channel_id):
    checker = ChessGameChecker(bot, discord_channel_id)
    return checker
