from datetime import datetime, timedelta

from commonlib.const import VAL_INVALID_ID
from sqlalchemy import and_

from commonlib.dbmodel.db_model import MUser, MRole, TSession, SPrivilegeFunction


class UserSql:
    @staticmethod
    def is_user_existing(db, id):
        """
        Check if user is existing in m_user table
        :param db: Database access object
        :type db: DbAccess
        :param id: user ID
        :type id: int
        :return: true: existing, false: not existing
        """
        cond = MUser.id == id
        ret = db.session.query(MUser.id).filter(cond).first()
        return ret is not None

    @staticmethod
    def has_privilege(db, user_info, function_id):
        """
        Check if user has privilege to use function
        :param db: Database access object
        :type db: DbAccess
        :param user_info: user info
        :type user_info: UserInfo
        :param function_id: function id
        :type function_id: member of commonlib.const.Function
        :return: has privilege：True, no privilege：False
        :rtype: boolean
        """
        privilege_id = VAL_INVALID_ID
        # Get user privilege
        privilege_info = db.session.query(MRole.privilege_id) \
            .join(MUser, MUser.role_id == MRole.id) \
            .filter(MRole.factory_id == user_info.factory_id,
                    MUser.id == user_info.user_id) \
            .first()
        if privilege_info is not None:
            privilege_id = privilege_info[0]
        # Select privilege
        db_id = db.session.query(SPrivilegeFunction.id) \
            .filter(and_(
                SPrivilegeFunction.privilege_id == privilege_id,
                SPrivilegeFunction.function_id == function_id,
            )) \
            .first()
        # has privilege：True, no privilege：False
        return db_id is not None


class TSessionSql:
    @staticmethod
    def get_session(db, session_key):
        """
        Get session info by specified session key
        :param db: Database access object
        :type db: DbAccess
        :param session_key: session key
        :type session_key: string
        :return: TSession of specified session key, None if invalid or expired session key
        :rtype: TSession
        """
        session_info = db.session.query(TSession) \
            .filter(TSession.key == session_key,
                    TSession.expired > datetime.now()) \
            .first()
        if session_info is None:
            return None
        return session_info

    @classmethod
    def reset_expire_time(cls, session_info, expired_time):
        """
        Reset session key expire datetime
        :param session_info: session info
        :type session_info: TSession
        :param expired_time: expired_time in seconds
        :type expired_time: int
        :return: -
        """
        session_info.expired = datetime.now() + timedelta(seconds=expired_time)
