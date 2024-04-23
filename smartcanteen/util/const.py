"""Constant Module"""
from enum import Enum

from config.config import SessionSetting
from config.message import ErrorMessage
from swagger_server.models.common_response import CommonResponse

class HTTPMethod(Enum):
    """Http method"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class LoginPath:
    OperationUi = '/login'


class CodeType(Enum):
    """Response code"""
    OK = (0, "OK")
    NG = (1, "NG")

    def __init__(self, code, title):
        """
        Constructor
        :param code: http code (int)
        :param title: response code ("OK"/"NG")
        """
        self.code = code
        self.title = title


class ReportType(Enum):
    """Report type"""
    STAFF_REPORT = (1, "STAFF_REPORT")
    DEPT_REPORT = (2, "DEPT_REPORT")
    SERVING_REPORT = (3, "SERVING_REPORT")

    def __init__(self, type, title):
        """
        Constructor
        :param type: report type (int)
        :param title: report title code (str)
        """
        self.type = type
        self.title = title


class Session:
    # Session timeout
    TIMEOUT = SessionSetting.SESSION_TIMEOUT
    # Key
    AUTH_KEY = 'Authorization'
    # Session key
    AUTH_SESSION_KEY = '_authentication'


class DefaultConst:
    UNKNOWN = "unknown"
    UNKNOWN_NUM = 0

    CONFIRMED = 1
    FLAG_ALL = 1
    TRUE = 1
    FALSE = 0
    OFF_SET_DAY = 0



class ResponseMessage(Enum):
    """
    Response definition（http_code, message, code)
    Use this class when make a response to client
    """
    Success = (200, "Success", "OK")
    SuccessInfo = (200, "Success", "OK")
    Fail = (400, "Fail", "NG")
    LoginRedirect = (302, "Redirect to login", "NG")
    InvalidArgument = (400, "Invalid param", "NG")
    AuthenticateFailed = (401, "Authentication error", "NG")
    UpdateProhibited = (403, "Update prohibited", "NG")
    NotExist = (404, "Not existing error", "NG")
    Conflict = (409, "Conflict error", "NG")
    ServerError = (500, "Server internal error", "NG")

    def __init__(self, http_code, message, code):
        """
        Constructor
        :param http_code: http code (int)
        :param message: response message (string)
        :param code: response code ("OK"/"NG")
        """
        self.http_code = http_code
        self.message = message
        self.code = code

    def make_response(self, parameter=None, message=None, info=None):
        """
        Create response
        :param parameter: parameter info (string)
        :param message: response message (string)
        :return: Swagger/Connexion response format: tuple(data, http_code)
        """
        if message is None:
            msg = self.message
        else:
            msg = message + ". " + self.message
        if parameter is not None:
            # If parameter is specified,
            # message format is: [http_code: [parameter]. [response message]]
            # Ex: "400: Parameter: user_name. Invalid parameter"
            return CommonResponse(
                self.code,
                "{0}: Parameter: {1}. {2}".format(str(self.http_code), parameter, msg),
                info), self.http_code
        # If parameter is not specified、
        # message format is: [http_code: [response message]]
        # Ex: "401: Authentication error"
        return CommonResponse(
            self.code,
            "{0}: {1}".format(str(self.http_code), msg),
            info), self.http_code

    @staticmethod
    def exception_response(exception):
        """
        Create exception response
        :param exception: exception happened (Exception)
        :return: Swagger/Connexion response format: tuple(data, http_code)
        """
        return ResponseMessage.ServerError.make_response(
            message=exception.__str__()
        )


class WebError(Exception):
    """
    Web error
    Use this call to raise and error on SmartCanteen web
    """
    def __init__(self, msg, original_exception=None):
        """
        :param msg: message
        :param original_exception: original exception
        """
        # message format is: [class name] [message]: [original exception]
        new_msg = "{0}-{1}".format(str(type(self).__name__), msg)
        if original_exception is not None:
            new_msg += ": "
            new_msg += str(original_exception)

        super(WebError, self).__init__(new_msg)

    def make_response(self, msg):
        """do nothing in base class"""
        pass


class LoginRedirect(WebError):
    """301: login redirect"""

    def make_response(self, msg):
        """override"""
        return ResponseMessage.LoginRedirect.make_response(
            message=msg)


class InvalidParamError(WebError):
    """400: parameter error"""

    def make_response(self, msg):
        """override"""
        return ResponseMessage.InvalidArgument.make_response(
            message=msg)


class ForbiddenError(WebError):
    """403: forbidden error"""

    def make_response(self, msg):
        """override"""
        return ResponseMessage.UpdateProhibited.make_response(
            message=msg)


class NotExistError(WebError):
    """404: not existing error"""

    def make_response(self, msg):
        """override"""
        return ResponseMessage.NotExist.make_response(message=msg)


class ConflictError(WebError):
    """409: conflict error"""

    def make_response(self, msg):
        """override"""
        return ResponseMessage.Conflict.make_response(message=msg)


class LoginError(WebError):
    """Login Error"""

    def make_response(self, msg):
        """override"""
        return ResponseMessage.Fail.make_response(message=ErrorMessage.LoginError)
