"""Authenticate"""
import time

import bcrypt
from decorator import decorator
from flask import g, request, redirect

from commonlib.auth import Auth, AuthenticateError
from commonlib.const import VAL_INVALID_ID, DbAccessError, UserInfo
from commonlib.db import DbAccess
from smartcanteen.util.common import WebDBUtil
from smartcanteen.util.const import DBRetryConst, Session, ResponseMessage, LoginPath
from smartcanteen.util.log import Logger


@decorator
def require_authenticate(func: callable, *args, **kwargs):
    """
    A decorator for view entry's authentication.
    :param func: decorate function
    :param args: args parameter of decorate function
    :param kwargs: kwargs parameter of decorate function
    :return: -
    """
    try:
        # get session key
        session_key = AuthUtil.get_key()
        if session_key is None or len(session_key) == 0:
            Logger.info("require_authenticate",
                        "Session key not found, redirect to login")
            return LoginUtil.redirect_login()

        # retry here if connection error
        for count in range(0, DBRetryConst.RETRY_COUNT + 1):
            try:
                with DbAccess.get_instance() as db_agent:
                    try:
                        db_agent.begin()
                        # commonlib authentication
                        user_info = Auth.api_authenticate(db_agent, session_key, Session.TIMEOUT)
                        db_agent.commit()
                        # store account info for later use (authorization, etc..)
                        LoginUtil.store_user_info(user_info)
                        break
                    except AuthenticateError as ex:
                        # authentication error
                        Logger.warning('require_authenticate', ex.__str__())
                        return LoginUtil.redirect_login()
                    except Exception:
                        # server error, DB error
                        WebDBUtil.db_rollback(db_agent, 'require_authenticate')
                        raise
            except (OperationalError, DBAPIError, DbAccessError) as ex:
                # DB error, retry if connection error
                if WebDBUtil.is_connection_valid(ex) or count == DBRetryConst.RETRY_COUNT:
                    raise
                Logger.warning("require_authenticate", ex.__str__())
                time.sleep(DBRetryConst.RETRY_INTERVAL)

        # OK, call decorate function
        return func(*args, **kwargs)

    except Exception as ex:
        # server error, DB error
        Logger.error("require_authenticate", Logger.traceback(ex))
        return ResponseMessage.ServerError.http_code


def require_authorize(db_agent, function_name):
    """
    Authorization processing: check if user has privilege to use function
    :param db_agent: Database access object
    :type db_agent: DbAccess
    :param function_name: function name
:type function_name: string
    :return: -
    """
    Auth.api_authorize(db_agent, LoginUtil.get_user_info(), function_name)


class AuthUtil:
    """Auth utility"""

    @classmethod
    def set_cookie(cls, response, key_str, session_key):
        response.set_cookie(key_str, session_key)

    @classmethod
    def get_key(cls):
        key = cls.get_session_key_from_cookie()
        if key is None:
            key = cls.get_session_key_from_header()
        return key

    @classmethod
    def get_session_key_from_cookie(cls):
        if Session.AUTH_SESSION_KEY in request.cookies:
            return request.cookies[Session.AUTH_SESSION_KEY]

    @classmethod
    def get_session_key_from_header(cls):
        if Session.AUTH_KEY in request.headers:
            return request.headers[Session.AUTH_KEY]


class LoginUtil:
    """Login utility"""

    @classmethod
    def redirect_login(cls):
        """
        Redirect to login view
        :return: -
        """
        return None, ResponseMessage.LoginRedirect.http_code

    @classmethod
    def hash_password(cls, password):
        """
        Encrypt password with bcrypt
        :type password: str
        :param password:
        :rtype: str
        :return:  encrypted password
        """
        return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(4))

    @classmethod
    def password_match(cls, password, hash_password):
        """
        Compare normal password with hash_password (encrypted password)
        :type password: str
        :param password: login password
        :type hash_password: str
        :param hash_password: hashed password
        :rtype: bool
        :return: True: matched, False: mismatched
        """
        if password is None or hash_password is None:
            return False
        return bcrypt.checkpw(password.encode('utf8'),
                              hash_password.encode('utf8'))

    @classmethod
    def store_user_info(cls, user_info):
        """
        Save user id to request info (flask.g)
        http://flask.pocoo.org/docs/0.12/api/#application-globals
        http://flask.pocoo.org/docs/0.12/appcontext/#locality-of-the-context
        :param user_info: user info
        :type user_info: UserInfo
        :return: -
        """
        g.user_info = user_info

    @classmethod
    def get_user_info(cls):
        """
        Get user id from request info (flask.g)
        http://flask.pocoo.org/docs/0.12/api/#application-globals
        http://flask.pocoo.org/docs/0.12/appcontext/#locality-of-the-context
        :return: user info
        :rtype: UserInfo
        """
        return getattr(g, 'user_info', None)

    @classmethod
    def get_factory_id(cls):
        """
        Get factory id from request info (flask.g)
        http://flask.pocoo.org/docs/0.12/api/#application-globals
        http://flask.pocoo.org/docs/0.12/appcontext/#locality-of-the-context
        :return: user info
        :rtype: int
        """
        user_info = cls.get_user_info()
        if user_info is not None:
            return user_info.factory_id

