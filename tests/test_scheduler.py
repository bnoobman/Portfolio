from unittest.mock import MagicMock

import pytest
from src.bnoobot.scheduler import Scheduler, ScheduledEvent
import datetime


@pytest.fixture
def scheduler(bot):
    logger = MagicMock()
    return Scheduler(bot, logger)


@pytest.mark.asyncio
async def test_schedule_event(scheduler, mock_channel):
    event_name = "Test Event"
    delay_minutes = 1
    description = "A test event"

    await scheduler.schedule_event(event_name, mock_channel, delay_minutes, description)

    assert len(scheduler.scheduled_events) == 1
    event = scheduler.scheduled_events[0]
    assert event.event_name == event_name
    assert event.channel == mock_channel
    assert event.description == description


@pytest.mark.asyncio
async def test_list_scheduled_events(scheduler, mock_channel):
    scheduler.scheduled_events.append(ScheduledEvent("Test Event", mock_channel, datetime.datetime.utcnow()))
    events = scheduler.list_scheduled_events()

    assert len(events) == 1
    assert events[0].event_name == "Test Event"

# todo add test for checking if remove_event function works