import uuid

from datetime import datetime, timedelta

from flask import Response, make_response
from swagger_server.models import UserInfo, LoginResponse
from werkzeug.utils import redirect

from commonlib.const import Function
from commonlib.db import DbAccess
from commonlib.dbmodel.db_model import TSession
from config.message import ErrorMessage
from smartcanteen.util.auth import AuthUtil
from smartcanteen.util.common import Util
from smartcanteen.util.const import ResponseMessage, WebError, Session, InvalidParamError
from smartcanteen.util.log import Logger
from smartcanteen.util.sql import TSessionSql


class LogoutLogic:

    @classmethod
    @Util.system_error_handler
    def logout_post(cls):
        """
        Do logout
        :rtype: CommResponse
        :return: Logout result
        """
        with DbAccess.get_instance() as db_agent:
            try:
                # Begin transaction
                db_agent.begin()
                login_id = cls.__do_logout(db_agent)
                db_agent.commit()
                Logger.info(Function.logout_post.name, "Logout succeeded, id={}".format(login_id))
                # Make info to response
                return Util.make_json_response(session_key=''), ResponseMessage.Success.http_code
            except WebError as ex:
                #  logout error
                Logger.warning(Function.login_post.name, ex.__str__())
                db_agent.rollback()
                return ResponseMessage.AuthenticateFailed.http_code

    @classmethod
    def __do_logout(cls, db_agent):
        """
        Do login:
            Check get account ID by login ID from database
            Check account ID with certificate
            Check password
        :param db_agent: DB access object
        :type db_agent: DBAccess
        :rtype: int
        :return: logout id
        """
        logout_id = None
        session_key = AuthUtil.get_key()
        # get session from DB
        session_info = TSessionSql.get_session_by_key(db_agent, session_key)
        if session_info is not None:
            logout_id = session_info.user_id
            # delete session
            db_agent.session.delete(session_info)
        return logout_id

    @classmethod
    def __create_new_session_key(cls, db_agent, factory_id, user_id):
        """
        Create new session key for login user
        :param db_agent: DB access instance
        :type db_agent: DBAccess
        :type factory_id: int
        :param factory_id: factory user id
        :type user_id: int
        :param user_id: login user id
        :rtype: str
        :return: user session key
        """
        # Delete all existing user session keys.
        cls._delete_session_key(db_agent, user_id)

        # Random a new session key
        session_key = "{}{}".format(user_id, uuid.uuid4().__str__())
        # Login is only available from one device
        # Login is available from multi tab

        # Insert session key to database
        cls.__insert_session_key(db_agent, factory_id, user_id, session_key)
        return session_key

    @classmethod
    def _delete_session_key(cls, db_agent, user_id):
        """
        Delete session key
        :type db_agent: DBAccess
        :param db_agent: DB access object
        :type user_id: int
        :param user_id: account id
        :return:-
        """
        session = TSessionSql.get_session(db_agent, user_id)
        if session is not None:
            db_agent.session.delete(session)

    @classmethod
    def __insert_session_key(cls, db_agent, factory_id, user_id, session_key):
        """
        Add session key to database
        :type db_agent: DBAccess
        :param db_agent: DB access object
        :type factory_id: int
        :param factory_id: factory id
        :type user_id: int
        :param user_id: account id
        :type session_key: str
        :param session_key: login user session key
        :return: -
        """
        new_session = TSession()
        new_session.key = session_key
        new_session.factory_id = factory_id
        new_session.user_id = user_id
        new_session.created = datetime.today()
        new_session.expired = datetime.now() + timedelta(seconds=Session.TIMEOUT)
        db_agent.session.add(new_session)

    @classmethod
    def __ensure_login_request(cls, db, login_request):
        if login_request is None:
            raise InvalidParamError("login_request is None")
        if login_request.login_id is None:
            raise InvalidParamError("login_id is None")
        if login_request.password is None:
            raise InvalidParamError("password is None")
