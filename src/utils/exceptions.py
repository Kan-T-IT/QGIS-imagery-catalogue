"""Custom exceptions module."""

import sys

from utils.constants import MessageType
from utils.helpers import tr


class PluginError(Exception):
    """Base class for custom exceptions."""

    def __init__(self, message='', message_type=MessageType.CRITICAL):
        self.message_type = message_type
        self.message = message
        print(f'{message} \n {str(sys.exc_info()[2])}')
        super().__init__(self.message)


class ProviderError(PluginError):
    """Custom exception for provider related errors."""

    def __init__(self, message=tr('Error to get results from provider.')):
        super().__init__(message, message_type=MessageType.INFO)


class HostError(PluginError):
    """Custom exception for host related errors."""

    def __init__(self, message=tr('Error to get results from host.')):
        super().__init__(message, message_type=MessageType.INFO)


class AuthorizationError(PluginError):
    """Custom exception for authorization related errors."""

    def __init__(self, message=tr('Error to get results from authorization.')):
        super().__init__(message, message_type=MessageType.WARNING)


class SettingsError(PluginError):
    """Custom exception for settings related errors."""

    def __init__(self, message=tr('Please check the plugin settings.')):
        super().__init__(message, message_type=MessageType.WARNING)


class DataNotFoundError(PluginError):
    """Custom exception for data related errors."""

    def __init__(self, message=tr('No data found.')):
        super().__init__(message, message_type=MessageType.INFO)
