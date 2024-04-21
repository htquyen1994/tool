""" Debug Log """
import inspect
import logging
import re
import time
import traceback
from logging.handlers import SysLogHandler, TimedRotatingFileHandler

from commonlib.const import Function, DbAccessError
# from commonlib.history import History
from config.config import LogSetting
from decorator import decorator
from flask import request
from smartcanteen.util.const import HTTPMethod, ResponseMessage, DBRetryConst

PATH = LogSetting.LOG_FILE

MESSAGE_FORMAT = "SMARTCANTEEN {}() {}"

# logger init
logger = logging.getLogger(PATH)
handler = TimedRotatingFileHandler(PATH, when="midnight", interval=1)
handler.suffix = "%Y%m%d"
handler.extMatch = re.compile(r"^\d{8}$")
process_info = '[%(asctime)s] [%(process)d-%(processName)s/%(thread)d-%(threadName)s] '
message_info = '%(levelname)s - %(message)s'
formatter = logging.Formatter(process_info + message_info)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class Logger:
    """ SmartCanteen log
    """
    @staticmethod
    def debug(function_name, message):
        """ DEBUG log
        :param function_name: function name
        :param message: message
        :return: -
        """
        logger.debug(MESSAGE_FORMAT.format(function_name, message))

    @staticmethod
    def info(function_name, message):
        """ INFO log
        :param function_name: function name
        :param message: message
        :return: -
        """
        logger.info(MESSAGE_FORMAT.format(function_name, message))

    @staticmethod
    def warning(function_name, message):
        """ WARN log
        :param function_name: function name
        :param message: message
        :return: -
        """
        logger.warning(MESSAGE_FORMAT.format(function_name, message))

    @staticmethod
    def error(function_name, message):
        """ ERROR log
        :param function_name: function name
        :param message: message
        :return: -
        """
        logger.error(MESSAGE_FORMAT.format(function_name, message))

    @staticmethod
    def traceback(exc):
        """
        Exception log
        :param exc: exception (Exception)
        :return: log format: error={[exception info]} tb={[traceback info]}
        """
        return "error={} tb={}".format(
            exc, traceback.format_tb(exc.__traceback__))


# API Log
class APILog:
    @staticmethod
    @decorator
    def require_log(f: callable, *args, **kwargs):
        """
        Decoratorとして、WepAPIを処理してAPIログを行う
        :param f: デコレートする関数
        :param args: デコレートする関数のargsパラメータ
        :param kwargs: デコレートする関数kwargsパラメータ
        :return: CommonModResponse
        """
        from smartcanteen.util.common import WebDBUtil
        func = getattr(Function, f.__name__)
        if func is None:
            func = Function.unknown
        parameters = list(inspect.signature(f).parameters.keys())
        log_input = dict(zip(parameters, args))
        try:
            res = f(*args, **kwargs)

            # no log for GET
            if request.method.strip().upper() == HTTPMethod.GET.value:
                return res

            # no log for authentication error
            if 1 < len(res):
                http_code = res[1]
            else:
                http_code = res[0]
            if ResponseMessage.AuthenticateFailed.http_code == http_code:
                return res

            # for count in range(0, DBRetryConst.RETRY_COUNT + 1):
            #     try:
            #         with DbAccess.get_instance() as db_agent:
            #             history_id = APILog.__exec_api_log(db_agent, func.__str__(), str(log_input), http_code)
            #             Logger.info("APILog", "Function {0}({1}) result {2} save to [t_history], id {3}"
            #                         .format(func.id(), func.__str__(), http_code, history_id))
            #         break
            #
            #     except (OperationalError, DBAPIError, DbAccessError) as ex:
            #         # retry on connection error
            #         if WebDBUtil.is_connection_valid(ex) or \
            #                 count == DBRetryConst.RETRY_COUNT:
            #             Logger.error("APILog", "ERROR: Write log failed {}".format(Logger.traceback(ex)))
            #             break
            #         # retry after interval
            #         if count == 0:
            #             Logger.warning("APILog", ex.__str__())
            #         time.sleep(DBRetryConst.RETRY_INTERVAL)
            #
            #     except Exception as exc:
            #         Logger.error("APILog", Logger.traceback(exc))
            #         break
            return res

        except Exception as ex:
            Logger.error("APILog", "ERROR: Write log failed {}".format(Logger.traceback(ex)))

    # @staticmethod
    # def __exec_api_log(db_agent, function_id, log_input, http_code):
    #     # from smartcanteen.util.auth import LoginUtil
    #     from smartcanteen.util.common import WebDBUtil
    #     try:
    #         # user_info = LoginUtil.get_user_info()
    #         # return History.write_history(db_agent, user_info.factory_id, user_info.user_id, function_id, http_code, log_input)
    #     except (DbAccessError):
    #         WebDBUtil.db_rollback(db_agent, "APILog")
    #         raise
