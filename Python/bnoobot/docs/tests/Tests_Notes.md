# Tests Notes

## Fixtures:

- bot_instance: Provides the bot object for testing.
- ctx: Mocks the Context object used in command invocations.

## Test Functions:

Each test function is decorated with @pytest.mark.asyncio to handle asynchronous test functions.
- test_ping_command: Tests the ping command to ensure it responds with 'Pong!'.
- test_hello_command: Tests the hello command to ensure it responds appropriately.
- test_kick_command: Mocks permissions and tests the kick command, checking that the kick method was called on the member.
- test_ban_command: Similar to kick, but for the ban command.
- test_unban_command_user_found: Tests unbanning a user that is found in the banned list.
- test_unban_command_user_not_found: Tests unbanning a user that is not found.
- test_mute_command: Tests muting a member and checks that the 'Muted' role is added.
- test_poll_command: Tests the poll command, ensuring that the poll message is sent and reactions are added.
- test_giveaway_command_no_entries: Tests the giveaway command when there are no entries.
- test_8ball_command: Tests the _8ball command with a mocked response.
- test_clear_command: Tests the clear command, ensuring messages are purged.

## Running the tests

In the app top level directory, run the following command:

Bash:
```bash
.venv/bin/pytest
```
Powershell:
```powershell
pytest.exe 
```

Add the `-s` flag if you want to see print statements or logs:

Bash:
```bash
.venv/bin/pytest -s
```

### Running tests with coverage reports

Bash:
```bash
.venv/bin/pytest --cov=src --cov-report=html --cov-report=term-missing
```

Powershell:
```powershell
pytest.exe --cov=.\src\bnoobot --cov-report=term --cov-report=html --cov-report=xml .\tests\
```

#### Coverage Columns Explained

- Name: File or module name.
- Stmts: Total statements.
- Miss: Statements missed (not executed).
- Branch: Total branches.
- BrPart: Partially executed branches.
- Cover: Overall coverage percentage.
- Missing: Line numbers of missing statements.

#### HTML Reports

Visual Representation: Color-coded source code showing which lines are covered.
- Green: Covered lines.
- Red: Missing lines.
- Yellow: Partial coverage (branches not fully covered).

### Mocking and Patching

#### Mocking discord.py Objects

The tests use MagicMock and AsyncMock to simulate discord.py objects like Context, Member, Guild, etc.

#### Patching External Calls

For functions that rely on external calls like `asyncio.sleep` or `random.choice`, we use unittest.mock.patch to control their behavior during tests.

### Important Considerations

#### Permissions 

When testing commands that require certain permissions, mock the guild_permissions attribute of the author to return True for the required permission.

#### Async Functions

Since discord.py uses async functions, tests must handle async calls appropriately.

#### Logger

If you want to test logging outputs, you can use the caplog fixture provided by pytest to capture log outputs.

Example:

```python
def test_some_logging_function(caplog):
    with caplog.at_level(logging.INFO):
        # Call your function that logs messages
        assert 'expected log message' in caplog.text
```

### Customizing Tests

#### Additional Commands

Add tests for any additional commands by following the patterns shown.

#### Error Handling

You can write tests to ensure that your error handling works as expected when users lack permissions or provide invalid inputs.

#### Testing Events

Testing event handlers (like on_ready) can be more complex but is possible using similar mocking techniques.

Example:

```python
@pytest.mark.asyncio
async def test_on_ready_event(bot_instance, caplog):
    with caplog.at_level(logging.INFO):
        await bot_instance.on_ready()
        assert f'Bot has logged in as {bot_instance.user}' in caplog.text
```

#### Example: Testing an Error Scenario

Here's how you might test the kick command when the user lacks permissions:

```python
@pytest.mark.asyncio
async def test_kick_command_no_permission(bot_instance, ctx):
    ctx.author.guild_permissions.kick_members = False
    member = MagicMock(spec=discord.Member)
    member.name = 'TestUser'
    with patch('logging.Logger.warning') as mock_logger:
        await bot_instance.get_command('kick').callback(ctx, member)
    ctx.send.assert_called_with("Sorry numbnuts, you don’t have the permission from Lord Bnoobman to do that...")
    mock_logger.assert_called()
```