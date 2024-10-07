import asyncio
import datetime
from typing import Optional, List

import discord


class ScheduledEvent:
    """Represents a scheduled event to be triggered at a specific time.

    Args:
        event_name (str): The name of the event.
        channel (discord.TextChannel): The Discord channel where the event will be announced.
        trigger_time (datetime.datetime): The time when the event will be triggered.
        description (Optional[str], optional): A description of the event. Defaults to None.
        attendees (Optional[List[str]], optional): A list of attendees for the event. Defaults to an empty list.
    """

    def __init__(self, event_name: str, channel: discord.TextChannel, trigger_time: datetime.datetime,
                 description: Optional[str] = None, attendees: Optional[List[str]] = None) -> None:
        self.event_name = event_name
        self.channel = channel
        self.trigger_time = trigger_time
        self.description = description
        self.attendees = attendees if attendees else []

    def __repr__(self) -> str:
        """Returns a string representation of the ScheduledEvent instance.

        Returns:
            str: A string representing the event, including its name, trigger time, description, and the number of attendees.
        """
        return f"Event({self.event_name}, {self.trigger_time}, {self.description}, Attendees: {len(self.attendees)})"


class Scheduler:
    """A class to manage scheduling, listing, and removing events.

    Args:
        bot (discord.ext.commands.Bot): The Discord bot instance.
        logger (logging.Logger): Logger instance for logging events.
    """

    def __init__(self, bot: discord.ext.commands.Bot, logger) -> None:
        """Initializes the Scheduler class with the bot and logger.

        Args:
            bot (discord.ext.commands.Bot): The Discord bot instance.
            logger (logging.Logger): Logger instance for logging scheduling events.
        """
        self.bot = bot
        self.logger = logger
        self.scheduled_events: List[ScheduledEvent] = []

    async def schedule_event(self, event_name: str, channel: discord.TextChannel, delay_minutes: int,
                             description: Optional[str] = None, attendees: Optional[List[str]] = None) -> None:
        """Schedules an event to be triggered after a specified delay.

        Args:
            event_name (str): The name of the event.
            channel (discord.TextChannel): The Discord channel where the event will be triggered.
            delay_minutes (int): The delay in minutes before the event triggers.
            description (Optional[str], optional): A description of the event. Defaults to None.
            attendees (Optional[List[str]], optional): A list of attendees (usernames or identifiers). Defaults to None.
        """
        delay_seconds = delay_minutes * 60
        trigger_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=delay_seconds)
        event = ScheduledEvent(event_name, channel, trigger_time, description, attendees)

        # Append the event to the internal list of scheduled events
        self.scheduled_events.append(event)
        self.logger.info(f"Scheduled event '{event_name}' for {trigger_time} (in {delay_minutes} minutes).")

        # Send a message to the channel announcing the event
        if event.description is not None:
            await channel.send(
                f"Scheduled event '{event_name}' with description:\n\n\t{description} \n\nto take place in: {delay_minutes} minutes.")
        else:
            await channel.send(f"Scheduled event '{event_name}' to take place in {delay_minutes} minutes.")

        # Wait for the specified delay before triggering the event
        await asyncio.sleep(delay_seconds)

        # Trigger the event
        await channel.send(f"The scheduled event `{event_name}` has been triggered!")

    def list_scheduled_events(self) -> List[ScheduledEvent]:
        """Returns a list of all currently scheduled events.

        Returns:
            List[ScheduledEvent]: A list of all scheduled events.
        """
        return self.scheduled_events

    def remove_event(self, event_name: str) -> bool:
        """Removes an event by its name from the scheduled events list.

        Args:
            event_name (str): The name of the event to remove.

        Returns:
            bool: True if the event was found and removed, False otherwise.
        """
        for event in self.scheduled_events:
            if event.event_name == event_name:
                self.scheduled_events.remove(event)
                self.logger.info(f"Event '{event_name}' removed from schedule.")
                return True
        self.logger.warning(f"Event '{event_name}' not found.")
        return False

    def find_event(self, event_name: str) -> Optional[ScheduledEvent]:
        """Finds and returns an event by its name.

        Args:
            event_name (str): The name of the event to find.

        Returns:
            Optional[ScheduledEvent]: The event if found, otherwise None.
        """
        for event in self.scheduled_events:
            if event.event_name == event_name:
                return event
        return None
