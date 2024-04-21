import uuid

from datetime import datetime, timedelta

from swagger_server.models import UserInfo, LoginResponse

from commonlib.const import Function
from smartcanteen.util.common import Util
from smartcanteen.util.const import ResponseMessage, WebError, LoginError, Session, InvalidParamError, DBConst
from smartcanteen.util.log import Logger


class LoginLogic:

    @classmethod
    @Util.system_error_handler
    def login_post(cls, login):
        try:
            cls.__ensure_login_request(login)
            # Begin transaction
            session_key = LoginLogic.__do_login(login.login_id, login.password)
            Logger.info(Function.login_post.name, "Login succeeded, id={}".format(login.login_id))
            # Make info to response
            access_info = cls.__get_access_info(login.login_id)
            login_res = LoginResponse(
                secret_key=session_key,
                # user_info=UserInfo(login_id=login.login_id, user_name=UserSql.get_user_name( login.login_id)),
                access_info=access_info
            )
            return Util.make_json_response(login_res.to_dict(), session_key), ResponseMessage.Success.http_code
        except WebError as ex:
            #  login error
            Logger.warning(Function.login_post.name, ex.__str__())
            return ex.make_response(str(ex))


    @classmethod
    def __do_login(cls,  user_id, password):
        # get user id from DB
        # user_info = UserSql.get_user_info(db_agent, user_id)
        # if user_info is None:
        #     raise LoginError(ErrorMessage.LoginError)
        # user = user_info[0]
        # factory_id = user_info[1]
        # # compare password
        # if not LoginUtil.password_match(password, user.password):
        #     raise LoginError(ErrorMessage.LoginError)
        # # create new session key
        return cls.__create_new_session_key(user_id)

    @classmethod
    def __create_new_session_key(cls,  user_id):
        """
        Create new session key for login user
        :param db_agent: DB access instance

        :type user_id: int
        :param user_id: login user id
        :rtype: str
        :return: user session key
        """
        # Delete all existing user session keys.

        # Random a new session key
        session_key = "{}{}".format(user_id, uuid.uuid4().__str__())
        # Login is only available from one device
        # Login is available from multi tab

        # Insert session key to database
        # cls.__insert_session_key(db_agent, factory_id, user_id, session_key)
        return session_key

    @classmethod
    def _delete_expired_session_key(cls, db_agent):
        """
        Delete expired session key
        :type db_agent: DBAccess
        :param db_agent: DB access object
        :return:-
        """
        TSessionSql.delete_expired_key(db_agent)

    @classmethod
    def __insert_session_key(cls, factory_id, user_id, session_key):
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
        # new_session = TSession()
        # new_session.key = session_key
        # new_session.factory_id = factory_id
        # new_session.user_id = user_id
        # new_session.created = datetime.today()
        # new_session.expired = datetime.now() + timedelta(seconds=Session.TIMEOUT)
        # db_agent.session.add(new_session)

    @classmethod
    def __ensure_login_request(cls, login_request):
        if login_request is None:
            raise InvalidParamError("login_request is None")
        if login_request.login_id is None:
            raise InvalidParamError("login_id is None")
        if login_request.password is None:
            raise InvalidParamError("Password is None")
        else:
            Util.ensure_length_str("password", login_request.password)

    @classmethod
    def __get_access_info(cls,  login_id):
        ret = []
        return ret

    @classmethod
    def __get_menu_privilege_dict(cls,privilege_id):
        ret = {}
        return ret
