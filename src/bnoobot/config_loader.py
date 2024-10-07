import logging.config
import os
from typing import Any, Dict

import yaml


class ConfigLoader:
    """A class to load configuration and logging settings from YAML files.

    Args:
        script_dir (str): The directory of the script where configuration files are located.
    """

    def __init__(self, script_dir: str) -> None:
        """Initializes the ConfigLoader with paths to configuration and logging files.

        Args:
            script_dir (str): The directory where the main script is located.
        """
        self.script_dir = script_dir
        self.config_dir = os.path.join(script_dir, 'config')
        self.app_config_path = os.path.join(self.config_dir, 'config.yaml')
        self.logging_config_path = os.path.join(self.config_dir, 'logging_config.yaml')

        self._load_logging_config()
        self.config = self._load_config()

    def _load_logging_config(self) -> None:
        """Loads the logging configuration from a YAML file."""
        with open(self.logging_config_path, 'r') as file:
            config = yaml.safe_load(file)
            logging.config.dictConfig(config)
        self.logger = logging.getLogger('discord')

    def _load_config(self) -> Dict[str, Any]:
        """Loads the application configuration from a YAML file.

        Returns:
            Dict[str, Any]: The configuration as a dictionary.
        """
        with open(self.app_config_path, 'r') as file:
            return yaml.safe_load(file)

    def get_config(self) -> Dict[str, Any]:
        """Returns the loaded configuration.

        Returns:
            Dict[str, Any]: The application configuration as a dictionary.
        """
        return self.config

    def get_logger(self) -> logging.Logger:
        """Returns the logger instance.

        Returns:
            logging.Logger: The logger configured using the logging configuration file.
        """
        return self.logger
