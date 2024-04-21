from sqlalchemy.exc import DBAPIError, OperationalError
from commonlib.const import DbAccessError, Function
from commonlib.db import DbAccess
from commonlib.dbmodel.db_model import MUser
from smartcanteen.util.auth import require_authenticate, require_authorize, LoginUtil
from smartcanteen.util.common import Util
from smartcanteen.util.const import WebError, ResponseMessage, InvalidParamError, ConflictError, NotExistError, \
    DefaultConst
from smartcanteen.util.log import Logger, APILog
from smartcanteen.util.sql import UserSql, RoleSql
from swagger_server.models import UserGetResponse, UserDetail, Role
from swagger_server.models.user import User
import bcrypt


class UserLogic:
    @classmethod
    @require_authenticate
    @Util.system_error_handler
    def user_get(cls, role_id):
        """user get
        get list user
        :param role_id: Filter by role id
        :type role_id: str
        :rtype: tuple(UserGetResponse, http code)
        """
        with DbAccess.get_instance() as db:
            try:
                require_authorize(db, Function.user_get.__str__())
                return cls.__execute_user_get(db, role_id)
            except (OperationalError, DBAPIError, DbAccessError):
                # DB error: raise to retry in Util
                raise

    @classmethod
    def __execute_user_get(cls, db, role_id):
        factory_id = LoginUtil.get_factory_id()
        # get all role name
        role_dict = RoleSql.get_role_name_dict(db)
        # get user list from db
        db_ret = UserSql.get_user_list(db, role_id, factory_id)
        # response with user list
        resp = UserGetResponse()
        resp.user_list = []
        for item in db_ret:
            user = UserDetail()
            user.id = item.id
            user.name = item.name
            # role name
            role_name = DefaultConst.UNKNOWN
            if item.role_id in role_dict.keys():
                role_name = role_dict[item.role_id]
            user.role = Role(id=item.role_id, name=role_name)
            resp.user_list.append(user)
        return resp, ResponseMessage.Success.http_code

    @classmethod
    @require_authenticate
    @APILog.require_log
    @Util.system_error_handler
    def user_post(cls, user):
        """user add
        add one user
        :param user: user info to add
        :type user: user
        :rtype: tuple(CommResponse, http code)
        """
        with DbAccess.get_instance() as db:
            try:
                require_authorize(db, Function.user_post.__str__())
                cls.__ensure_user_post_request(db, user)
                cls.__ensure_conflict_user(db, user.id)
                # Begin transaction
                db.begin()
                cls.__execute_user_post(db, user)
                db.commit()
                return ResponseMessage.Success.make_response()
            except WebError as exc:
                Logger.warning(Function.user_post, exc.__str__())
                db.rollback()
                return exc.make_response(str(exc))
            except (OperationalError, DBAPIError, DbAccessError):
                # DB error: raise to retry in Util
                db.rollback()
                raise

    @classmethod
    def __execute_user_post(cls, db, user):
        password = user.password
        # Convert swagger model to DB model
        db_user = MUser()
        db_user.id = user.id
        db_user.name = user.name
        db_user.role_id = user.role_id
        if password is not None:
            db_user.password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(4))
        # Add to DB
        UserSql.add(db, db_user)

    @classmethod
    @require_authenticate
    @APILog.require_log
    @Util.system_error_handler
    def user_put(cls, id, user):
        """user edit
           edit one user
           :param id:
           :type id: str
           :param user: user info to add
           :type user: user
           :rtype: tuple(CommResponse, http code)
        """
        with DbAccess.get_instance() as db:
            try:
                require_authorize(db, Function.user_put.__str__())
                cls.__ensure_user_put_request(db, user, id=id)
                cls.__ensure_exist_user(db, id)
                # Begin transaction
                db.begin()
                cls.__execute_user_put(db, id, user)
                db.commit()
                return ResponseMessage.Success.make_response()
            except WebError as exc:
                Logger.warning(Function.user_put, exc.__str__())
                db.rollback()
                return exc.make_response(str(exc))
            except (OperationalError, DBAPIError, DbAccessError):
                # DB error: raise to retry in Util
                db.rollback()
                raise

    @classmethod
    def __execute_user_put(cls, db, id, user):
        # Convert swagger model to DB model
        db_user = MUser()
        if user.password is not None:
            db_user.password = bcrypt.hashpw(user.password.encode('utf8'), bcrypt.gensalt(4))
        else:
            db_user.name = user.name
            db_user.role_id = user.role_id
        # Edit to DB
        UserSql.update(db, id, db_user)

    @classmethod
    @require_authenticate
    @APILog.require_log
    @Util.system_error_handler
    def user_delete(cls, id) :
        """user delete
        delete one user
        :param id: user id to delete
        :type id: str
        :rtype: tuple(CommResponse, http code)
        """
        with DbAccess.get_instance() as db:
            try:
                require_authorize(db, Function.user_delete.__str__())
                cls.__ensure_exist_user(db, id)
                cls.__ensure_using_user(db, id)
                # Begin transaction
                db.begin()
                cls.__execute_user_delete(db, id)
                db.commit()
                return ResponseMessage.Success.make_response()
            except WebError as exc:
                Logger.warning(Function.user_delete, exc.__str__())
                db.rollback()
                return exc.make_response(str(exc))
            except (OperationalError, DBAPIError, DbAccessError):
                # DB error: raise to retry in Util
                db.rollback()
                raise

    @classmethod
    def __execute_user_delete(cls, db, id):
        return UserSql.delete(db, id)

    @classmethod
    def __ensure_user_post_request(cls, db, user):
        """
        validate user in post method
        :param db: db access object
        :type db: DbAccess
        :param user: user info
        :type user: User
        :return:
        """
        if user is None:
            raise InvalidParamError("User is None")
        if user.id is None:
            raise InvalidParamError("User id is None")
        if user.name is None:
            raise InvalidParamError("User name is None")
        else:
            Util.ensure_length_str("User name", user.name)
        if user.password is None:
            raise InvalidParamError("User password is None")
        else:
            Util.ensure_length_str("User password", user.password)
        if user.role_id is None:
            raise InvalidParamError("Value of role is None")
        else:
            # Check DB
            if not RoleSql.is_role_existing(db, user.role_id):
                raise InvalidParamError("Selected role is not existing")
            factory_id = RoleSql.get_factory_id(db, user.role_id)
            Util.ensure_factory_id(factory_id)

    @classmethod
    def __ensure_user_put_request(cls, db, user, id=None):
        """
        validate user in put method
        :param db: db access object
        :type db: DbAccess
        :param user: user info
        :type user: User
        :param id: user id to edit
        :type id: str
        :return:
        """
        if id is not None:
            Util.ensure_int("id", id)
        if user is None:
            raise InvalidParamError("User is None")
        # edit password only
        if user.password is not None:
            Util.ensure_length_str("User password", user.password)
        else:
            # do not edit password
            if user.name is None:
                raise InvalidParamError("User name is None")
            else:
                Util.ensure_length_str("User name", user.name)
            if user.role_id is None:
                raise InvalidParamError("Value of role is None")
            else:
                # Check DB
                if not RoleSql.is_role_existing(db, user.role_id):
                    raise InvalidParamError("Selected role is not existing")
                factory_id = RoleSql.get_factory_id(db, user.role_id)
                Util.ensure_factory_id(factory_id)

    @classmethod
    def __ensure_conflict_user(cls, db, id):
        # check if user is conflicting in db
        if UserSql.is_user_existing(db, id):
            # if existing, return ConflictError
            raise ConflictError("User id = " + str(id))

    @classmethod
    def __ensure_exist_user(cls, db, id):
        # check if user is existing in db
        if not(UserSql.is_user_existing(db, id)):
            # if not exist, return NotExistError
            raise NotExistError("User id = {0} not exist".format(id))

    @classmethod
    def __ensure_using_user(cls, db, id):
        pass
