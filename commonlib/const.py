"""Common definition"""
from enum import Enum

# Config file
CFG_FILENAME = "config.ini"

# Invalid user id
VAL_INVALID_ID = -1



class CommonLibError(Exception):
    """CommonLib error"""

    def __init__(self, msg, original_exception=None):
        """
        :param msg: message
        :param original_exception: original exception
        """
        # Message format = [Error class name] [message]: [original exception]
        new_msg = "{0}-{1}".format(str(type(self).__name__), msg)
        if original_exception is not None:
            new_msg += ": "
            new_msg += str(original_exception)

        super(CommonLibError, self).__init__(new_msg)


class NotFoundError(CommonLibError):
    """Not existing error"""


class ConfigError(CommonLibError):
    """Conflict error"""


class DbAccessError(CommonLibError):
    """Database error"""


class AuthenticateError(CommonLibError):
    """Authentication error"""


class AuthorizationError(CommonLibError):
    """Authentication error"""


class Function(Enum):
    """Web function definition"""

    def __str__(self):
        return self.name

    def id(self):
        """
        :rtype: int
        :return: Function ID
        """
        return self.value

    # unknown
    unknown = 0

    # auth function
    login_get = 1
    login_post = 2
    logout_post = 12


