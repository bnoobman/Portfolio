import pytest
from unittest.mock import AsyncMock, patch
from src.bnoobot.commands import (
    ping, hello, kick, ban, unban, mute, poll, _8ball, clear,
    schedule, list_events, remove_event, help_schedule
)


@pytest.mark.asyncio
async def test_ping(mock_context):
    await ping(mock_context)
    mock_context.send.assert_called_once_with('Pong!')


@pytest.mark.asyncio
async def test_hello(mock_context):
    await hello(mock_context)
    mock_context.send.assert_called_once_with(f'Hello, {mock_context.author}.')


@pytest.mark.asyncio
async def test_kick(mock_context):
    member = AsyncMock()
    member.name = "TestMember"
    await kick(mock_context, member, reason="Testing")
    mock_context.send.assert_called_once_with(f'{member.name} has been kicked for: Testing')
    member.kick.assert_called_once_with(reason="Testing")


@pytest.mark.asyncio
async def test_ban(mock_context):
    member = AsyncMock()
    member.name = "TestMember"
    await ban(mock_context, member, reason="Testing")
    mock_context.send.assert_called_once_with(f'{member.name} has been banned for: Testing')
    member.ban.assert_called_once_with(reason="Testing")


@pytest.mark.asyncio
async def test_unban(mock_context):
    user = "TestUser#1234"
    banned_user = AsyncMock()
    banned_user.name = "TestUser"
    banned_user.discriminator = "1234"
    mock_context.guild.bans = AsyncMock(return_value=[AsyncMock(user=banned_user)])
    mock_context.guild.unban = AsyncMock()
    await unban(mock_context, user=user)
    mock_context.guild.unban.assert_called_once_with(banned_user)
    mock_context.send.assert_called_once_with(f'{banned_user.name} has been unbanned.')


@pytest.mark.asyncio
async def test_mute(mock_context):
    member = AsyncMock()
    role = AsyncMock(name="Muted")
    mock_context.guild.roles = [role]
    mock_context.guild.create_role = AsyncMock(return_value=role)
    await mute(mock_context, member, reason="Spamming")
    member.add_roles.assert_called_once_with(role, reason="Spamming")
    mock_context.send.assert_called_once_with(f'{member.mention} has been muted for: Spamming')


@pytest.mark.asyncio
async def test_poll(mock_context):
    question = "Is Python awesome?"
    message = AsyncMock()
    mock_context.send = AsyncMock(return_value=message)
    await poll(mock_context, question=question)
    mock_context.send.assert_called_once_with(f'📊 Poll: {question}')
    message.add_reaction.assert_any_call('👍')
    message.add_reaction.assert_any_call('👎')


@pytest.mark.asyncio
@patch('src.bnoobot.commands.random.choice', return_value="Yes, definitely.")
async def test_8ball(mock_choice, mock_context):
    question = "Will I learn Python?"
    await _8ball(mock_context, question=question)
    mock_context.send.assert_called_once_with(f'Question: {question}\nAnswer: Yes, definitely.')


@pytest.mark.asyncio
async def test_clear(mock_context):
    amount = 10
    mock_context.channel.purge = AsyncMock()
    await clear(mock_context, amount=amount)
    mock_context.channel.purge.assert_called_once_with(limit=amount)
    mock_context.send.assert_called_once_with(f'Deleted {amount} messages.', delete_after=5)


@pytest.mark.asyncio
async def test_schedule(mock_context):
    mock_context.bot.scheduler.schedule_event = AsyncMock()
    event_name = "Test Event"
    delay_minutes = 5
    description = "This is a test event."
    await schedule(mock_context, event_name=event_name, delay_minutes=delay_minutes, description=description)
    mock_context.bot.scheduler.schedule_event.assert_called_once_with(
        event_name, mock_context.channel, delay_minutes, description
    )


@pytest.mark.asyncio
async def test_list_events(mock_context):
    mock_event = AsyncMock(event_name="Test Event", trigger_time="Tomorrow")
    mock_context.bot.scheduler.list_scheduled_events = AsyncMock(return_value=[mock_event])

    await list_events(mock_context)

    # Verify the correct message is sent for the event
    mock_context.send.assert_any_call(f"Event: {mock_event.event_name}, Scheduled for: {mock_event.trigger_time}")



@pytest.mark.asyncio
async def test_remove_event_success(mock_context):
    mock_context.bot.scheduler.remove_event = AsyncMock(return_value=True)
    event_name = "Test Event"
    await remove_event(mock_context, event_name=event_name)
    mock_context.send.assert_called_once_with(f"Event '{event_name}' has been removed from the schedule.")


@pytest.mark.asyncio
async def test_remove_event_failure(mock_context):
    # Mock the scheduler's `remove_event` to return False (simulate failure to find the event)
    mock_context.bot.scheduler.remove_event = AsyncMock(return_value=False)

    event_name = "Nonexistent Event"

    await remove_event(mock_context, event_name=event_name)

    # Verify that the correct failure message is sent
    mock_context.send.assert_called_once_with(f"Event '{event_name}' not found.")


@pytest.mark.asyncio
async def test_help_schedule(mock_context):
    expected_message = (
        "One Hour is equal to: 60 Min\n"
        "Three Hours is equal to: 180 Min\n"
        "One Day is equal to: 1440 Min\n"
        "Two Days is equal to: 2880 Min\n"
        "Three Days is equal to: 4320 Min\n"
        "One Week is equal to: 10080 Min"
    )
    await help_schedule(mock_context)
    mock_context.send.assert_called_once_with(expected_message)
