"""Common Module"""
import datetime
import json
import time

from datetime import timedelta, time
from decorator import decorator
from flask import request, make_response

from commonlib.const import AuthenticateError, AuthorizationError
# from commonlib.db import DbUtil
from smartcanteen.util.const import (ResponseMessage,
                                     DBRetryConst,
                                     HTTPMethod, InvalidParamError, Session, DBConst, DefaultConst)
from smartcanteen.util.log import Logger


class Util:
    """Util"""

    @staticmethod
    @decorator
    def system_error_handler(f: callable, *args, **kwargs):
        """
        Decorator function to system error for all APIs
        :param f: decorator function
        :param args: decorator args
        :param kwargs: decorator kwargs
        :rtype: tuple
        :return: Swagger/ConnexionのResponse return format: tuple(data, http_code)
                data: CommonResponse
                http_code: http code
        """
        function_name = f.__name__
        for count in range(0, DBRetryConst.RETRY_COUNT + 1):
            try:
                return f(*args, **kwargs)

            except Exception as ex:
                # Database error
                Logger.error(function_name, "{} {}".format(str(ex), Logger.traceback(ex)))
                return Util.__error_response(ex)

    @staticmethod
    def __error_response(exception):
        return ResponseMessage.exception_response(exception)

    @staticmethod
    def __auth_error_response(exception):
        return ResponseMessage.AuthenticateFailed.make_response(message=str(exception))

    @staticmethod
    def ensure_int(var_name, var_value):
        try:
            return int(var_value)
        except Exception:
            raise InvalidParamError("{0}:{1}".format(var_name,var_value))

    @staticmethod
    def ensure_length_str(var_name, var_value):
        try:
            len_str = len(var_value)
            if len_str > 256:
                raise
            return
        except Exception as ex:
            raise InvalidParamError("Length of {0} > 256 characters".format(var_name))

    @staticmethod
    def ensure_factory_id(factory_id):
        from smartcanteen.util.auth import LoginUtil
        user_factory_id = LoginUtil.get_factory_id()
        if user_factory_id is not None:
            if user_factory_id != factory_id:
                raise InvalidParamError("factory_id = {0} is not match with user.factory_id ({1})".format(factory_id, user_factory_id))

    @staticmethod
    def make_json_response(body=None, session_key=None):
        """
        Validate value is int
        :type body: dict
        :param body: response body
        :type session_key: str
        :param session_key: session key
        :rtype: Response
        :return: response
        """
        if body is None:
            res = make_response()
        else:
            json_body = json.dumps(body)
            res = make_response(json_body)
            res.mimetype = 'application/json'
        if session_key is not None:
            from smartcanteen.util.auth import AuthUtil
            AuthUtil.set_cookie(res, Session.AUTH_SESSION_KEY, session_key)
        return res

    @staticmethod
    def convert_date_to_format(str_date, str_format):
        from datetime import datetime
        if type(str_date) != str:
            return str_date
        try:
            dt = datetime.strptime(str_date, str_format)
        except Exception:
            dt = datetime.strptime(str_date, str_format)
        return dt

    @staticmethod
    def convert_datetime_to_date(str_date, str_format):
        import datetime
        date_ret = Util.convert_date_to_format(str_date, str_format)
        ret = datetime.datetime(date_ret.year, date_ret.month, date_ret.day)
        return ret.date()

    @staticmethod
    def get_month_range(str_date):
        import calendar
        date = Util.convert_date_to_format(str_date, "%Y-%m")
        date = date.replace(day=1)
        end_of_month = calendar.monthrange(date.year, date.month)[1]
        return datetime.datetime(date.year, date.month, 1), datetime.datetime(date.year, date.month, end_of_month)

    # get shift

class WebDBUtil():
    @classmethod
    def log_error(cls, function_name, exception):
        Logger.error(function_name, Logger.traceback(exception))
