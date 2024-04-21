
from commonlib.const import CommonLibError, AuthenticateError, AuthorizationError, Function, UserInfo
from commonlib.sql import UserSql, TSessionSql


class Auth:

    @staticmethod
    def api_authenticate(db_agent, session_key, expired_time=None):
        """
        Check if session key is valid (existing and not expired)
        If session is valid, update expired datetime
        :param db_agent: Database access object
        :type db_agent: DBAccess
        :param session_key: Session key
        :type session_key: string
        :param expired_time: expired_time in seconds
        :type expired_time: int
        :return: OK：user id, NG：raise AuthenticateError exception
        """
        try:
            session_info = TSessionSql.get_session(db_agent, session_key)

            if session_info is None:
                # invalid session key, raise exception
                raise CommonLibError("Invalid Session Key")
            if expired_time is not None:
                # reset expired time
                TSessionSql.reset_expire_time(session_info, expired_time)
            # return user id
            return UserInfo(session_info.factory_id, session_info.user_id)

        except Exception as ex:
            raise AuthenticateError(str(ex))

    @staticmethod
    def api_authorize(db_agent, user_info, function_name):
        """
        Check if user has privilege to use function
        :param db_agent: Database access object
        :type db_agent: DBAccess
        :param user_info: user info (get from api_authenticate() function)
        :type user_info: UserInfo
        :param function_name: function name
        :type function_name: member of commonlib.const.Function
        :return: -
        """
        try:
            if user_info is None:
                raise Exception("Access Forbidden")

            # Convert function name to function id
            function_id = Function[function_name].id()

            # Check if user has privilege to use function
            if not UserSql.has_privilege(db_agent, user_info, function_id):
                raise Exception("Access Forbidden")
        except Exception as ex:
            raise AuthorizationError(ex.__str__())
