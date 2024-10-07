import pytest
import os
from unittest.mock import patch, mock_open, MagicMock
from src.bnoobot.config_loader import ConfigLoader


# Test 1: Test initialization (__init__)
@patch('src.bnoobot.config_loader.ConfigLoader._load_logging_config')
@patch('src.bnoobot.config_loader.ConfigLoader._load_config', return_value={'key': 'value'})
def test_config_loader_init(mock_load_config, mock_load_logging_config):
    script_dir = os.path.join('src', 'bnoobot')
    loader = ConfigLoader(script_dir)

    # Use os.path.join to handle platform-specific path separators
    assert loader.script_dir == script_dir
    assert loader.config_dir == os.path.join(script_dir, 'config')
    assert loader.app_config_path == os.path.join(script_dir, 'config', 'config.yaml')
    assert loader.logging_config_path == os.path.join(script_dir, 'config', 'logging_config.yaml')

    # Verify methods were called
    mock_load_logging_config.assert_called_once()
    mock_load_config.assert_called_once()
    assert loader.config == {'key': 'value'}


# Test 2: Test _load_logging_config
@patch('yaml.safe_load', return_value={'version': 1, 'handlers': {}, 'loggers': {}, 'root': {}})
@patch('logging.config.dictConfig')
@patch('builtins.open', new_callable=mock_open, read_data="version: 1")
def test_load_logging_config(mock_file, mock_dict_config, mock_yaml_load):
    loader = ConfigLoader('src/bnoobot')

    # Ensure the logging config file is read correctly
    mock_file.assert_any_call(loader.logging_config_path, 'r')
    # Check that yaml.safe_load is called twice (once for logging config and once for app config)
    assert mock_yaml_load.call_count == 2  # Adjust to check two calls
    mock_dict_config.assert_called_once_with({'version': 1, 'handlers': {}, 'loggers': {}, 'root': {}})


# Test 3: Test _load_config (with logging config mocked out)
@patch('src.bnoobot.config_loader.ConfigLoader._load_logging_config')  # Mock out logging config
@patch('yaml.safe_load', return_value={'app_key': 'app_value'})
@patch('builtins.open', new_callable=mock_open, read_data="app_key: app_value")
def test_load_config(mock_file, mock_yaml_load, mock_load_logging_config):
    loader = ConfigLoader('src/bnoobot')

    # Ensure the app config file is read correctly
    mock_file.assert_any_call(loader.app_config_path, 'r')
    mock_yaml_load.assert_called()  # We don't care how many times it is called in this case
    assert loader._load_config() == {'app_key': 'app_value'}


# Test 4: Test get_config
@patch('builtins.open', new_callable=mock_open, read_data="app_key: app_value")
@patch('src.bnoobot.config_loader.ConfigLoader._load_logging_config')
def test_get_config(mock_load_logging_config, mock_file):
    loader = ConfigLoader('src/bnoobot')
    loader.config = {'some_key': 'some_value'}

    # Ensure get_config returns the correct configuration
    assert loader.get_config() == {'some_key': 'some_value'}


# Test 5: Test get_logger
@patch('builtins.open', new_callable=mock_open, read_data="version: 1")
@patch('src.bnoobot.config_loader.ConfigLoader._load_logging_config')
def test_get_logger(mock_load_logging_config, mock_file):
    loader = ConfigLoader('src/bnoobot')
    loader.logger = MagicMock()

    # Ensure get_logger returns the logger instance
    assert loader.get_logger() == loader.logger
