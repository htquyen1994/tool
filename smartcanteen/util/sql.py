from sqlalchemy import func, extract, distinct, or_, and_, tuple_

from commonlib.const import DbDefault, VAL_INVALID_ID
from commonlib.db import DbAccess
from commonlib.dbmodel.db_model import MUser, MRole, MLine, MMeal, MScanner, SFunction, \
    TSession, SPrivilege, SFactory, MShiftMealServing, MServing, TStaffServing, TStaffRegister, MLineShiftMealServing, \
    MShift, TDepartment, TStaff, TStaffFinger, TProductLine, RKitchen, MUserDepartment, MUserProductLine, \
    MKitchenStatusRegistration, MKitchenHistory, MCalendar, SPrivilegeMenu, SMenu, TPrimeDepartment, \
    MGroupLineShiftMealServing
from commonlib.dbmodel.db_model import MShiftMeal, MLineScanner
from datetime import datetime

from smartcanteen.util.const import DBConst


def exec_query_get_list(query, condition, in_list):
    # because of pyodbc LIMITATION, do query on max 2100 parameter
    ret_list = []
    cnt = 0
    while cnt * DBConst.MAX_PARAM_COUNT <= len(in_list):
        start = cnt * DBConst.MAX_PARAM_COUNT
        end = ((cnt+1) * DBConst.MAX_PARAM_COUNT)
        if end >= (len(in_list)):
            end = len(in_list)
        cnt = cnt + 1
        # query partial list
        tmp_list = in_list[start:end]
        db_tmp_list = query.filter(condition.in_(tmp_list)).all()
        ret_list.extend(db_tmp_list)
    return ret_list


class FactorySql:
    @staticmethod
    def get_factory_list(db, id=None):
        """
        Get list of factory in s_factory table
        :param db: Database access object
        :param id: factory_id
        :return: [SFactory]
        """
        query = db.session.query(SFactory)
        if id is not None:
            query = query.filter(SFactory.id == id)
        ret = query.all()
        return ret

    @staticmethod
    def get_factory_name(db, id):
        """
        Get name of all factory in s_factory table
        :param db: Database access object
        :param id: factory_id
        :return: Dict of name {id: name}
        """
        ret = db.session.query(SFactory.name).filter(SFactory.id == id).first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def get_factory_name_dict(db):
        """
        Get name of one factory in s_factory table
        :param db: Database access object
        :param id: factory_id
        :return: Factory name
        """
        query = db.session.query(SFactory)
        db_ret = query.all()
        ret = {}
        if db_ret is not None:
            for item in db_ret:
                ret[item.id] = item.name
        return ret

    @staticmethod
    def is_factory_existing(db, id):
        """
        Check existing of one factory in s_factory table
        :param db: Database access object
        :param id: factory_id
        :return: true: existing, false: not existing
        """
        ret = db.session.query(SFactory.id).filter(SFactory.id == id).first()
        return ret is not None


# Class PrivilegeSql
class PrivilegeSql:
    @staticmethod
    def get_privilege_list(db, init_privilege=None):
        """
        Get list of privilege in s_privilege table
        :param db: Database access object
        :param init_privilege: init_privilege
        :return: [SPrivilege]
        """
        query = db.session.query(SPrivilege)
        if init_privilege is not None:
            query = query.filter(SPrivilege.init_privilege == init_privilege)
        ret = query.all()
        return ret

    @staticmethod
    def get_privilege_name(db, id):
        """
        Get name of one privilege in s_privilege table
        :param db: Database object access
        :param id: privilege id
        :return: Privilege name
        """
        ret = db.session.query(SPrivilege.name).filter(SPrivilege.id == id).first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def get_privilege_name_dict(db):
        """
        Get all privilege name in s_privilege table
        :param db: Database access object
        :return: Dict of privilege name {id: name}
        """
        query = db.session.query(SPrivilege)
        db_ret = query.all()
        ret = {}
        if db_ret is not None:
            for item in db_ret:
                ret[item.id] = item.name
        return ret

    @staticmethod
    def is_privilege_existing(db, id):
        """
        Check if privilege is existing in s_privilege table
        :param db: Database object access
        :param id: privilege id
        :return: true: existing, false: not existing
        """
        ret = db.session.query(SPrivilege.id).filter(SPrivilege.id == id).first()
        return ret is not None


#  Class UserSql
class UserSql:
    @staticmethod
    def get_user_list(db, role_id, factory_id):
        """
        Get list of all user in m_user table
        :param db: Database object access
        :param role_id: role id
        :param factory_id: factory_id
        :return: [m_user]
        """
        query = db.session.query(MUser)\
            .join(MRole, MUser.role_id == MRole.id)
        if role_id is not None:
            query = query.filter(MRole.id == role_id)
        if factory_id is not None:
            query = query.filter(MRole.factory_id == factory_id)
        ret = query.all()
        return ret

    @staticmethod
    def get_user_name_dict(db, factory_id):
        """
        Get dict of all user in m_user table
        :param db: Database object access
        :param factory_id: factory_id
        :return: user dict {id, name}
        """
        query = db.session.query(MUser.id, MUser.name)\
            .join(MRole, MUser.role_id == MRole.id)
        if factory_id is not None:
            query = query.filter(MRole.factory_id == factory_id)
        ret = query.all()
        ret_dict = {}
        if ret is not None:
            for item in ret:
                ret_dict[item[0]] = item[1]
        return ret_dict

    @staticmethod
    def get_user_info(db, id):
        """
        Get user specified by id in m_user table
        :param db: Database object access
        :param id: user id
        :return: tuple(MUser, factory_id)
        """
        ret = db.session.query(MUser, MRole.factory_id) \
            .join(MRole, MUser.role_id == MRole.id) \
            .filter(MUser.id == id).first()
        if ret is not None:
            return ret

    @staticmethod
    def get_user_name(db, id):
        """
        Get user name specified by id in m_user table
        :param db: Database object access
        :param id: user id
        :return: user name (str)
        """
        ret = db.session.query(MUser.name) \
            .filter(MUser.id == id).first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def is_user_existing(db, id):
        """
        Check if user is existing in m_user table
        :param db: Database object access
        :param id: user id
        :return: true: existing, false: not existing
        """
        ret = db.session.query(MUser.id).filter(MUser.id == id).first()
        return ret is not None

    @staticmethod
    def is_role_existing(db, role_id):
        """
        Check if role is existing in m_user table
        :param db: Database object access
        :param role_id: role id
        :return: true: existing, false: not existing
        """
        ret = db.session.query(MUser.id).filter(MUser.role_id == role_id).first()
        return ret is not None

    @staticmethod
    def add(db, user):
        """
        Add user to m_user table
        :param db: DbAccess object (DbAccess)
        :param user: user info (m_user model)
        :return:
        """
        user.created = datetime.now()
        user.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(user)

    @staticmethod
    def update(db, user_id, user):
        """
        Edit user to m_user table (name, password, role_id only)
        :param db: DbAccess object (DbAccess)
        :param user_id: id user info(m_user model)
        :param user: user info(m_user model)
        :return:
        """
        db_user = db.session.query(MUser).filter_by(id=user_id).first()
        if user.password is not None:
            db_user.password = user.password
        else:
            db_user.name = user.name
            db_user.role_id = user.role_id
        # auto update
        db_user.modified = datetime.now()
        db_user.upd_count = (db_user.upd_count + 1) if db_user.upd_count is not None else DbDefault.UPDATED_COUNT.value

    @staticmethod
    def delete(db, user_id):
        """
        delete user
        :param db: DbAccess object (DbAccess)
        :param user_id: id user info(m_user model)
        :return:
        """
        db.session.query(MUser).filter(MUser.id == user_id).delete()

    @staticmethod
    def get_privilege(db, user_id):
        privilege_id = VAL_INVALID_ID
        # Get user privilege
        privilege_info = db.session.query(SPrivilege.id) \
            .join(MRole, MRole.privilege_id == SPrivilege.id) \
            .join(MUser, MUser.role_id == MRole.id) \
            .filter(MUser.id == user_id) \
            .first()
        if privilege_info is not None:
            privilege_id = privilege_info[0]
        return privilege_id


# Class RoleSql
class RoleSql:
    @staticmethod
    def get_role_list(db, factory_id, init_privilege):
        """
        Get list of all role in m_role table
        :param db: Database object access
        :param factory_id: factory id
        :param init_privilege: init_privilege
        :return: [MRole]
        """
        cond = 1 == 1
        if factory_id is not None:
            cond = MRole.factory_id == factory_id
        query = db.session.query(MRole)\
               .join(SPrivilege, SPrivilege.id == MRole.privilege_id)\
               .filter(cond)
        if init_privilege is not None:
            query = query.filter(SPrivilege.init_privilege == init_privilege)
        ret = query.all()
        return ret

    @staticmethod
    def get_role(db, id):
        """
        Get role specified by id in m_role table
        :param db: Database object access
        :param id: role id
        :return: [m_role]
        """
        ret = db.session.query(MRole).filter(MRole.id == id).first()
        return ret

    @staticmethod
    def get_role_name(db, id):
        """
        Get role name specified by id in m_role table
        :param db: Database object access
        :param id: role id
        :return: role name (str)
        """
        ret = db.session.query(MRole.name).filter(MRole.id == id).first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def get_role_name_dict(db):
        """
        Get all role name in m_role table
        :param db: Database object access
        :param id: role id
        :return: role name dict {id: name}
        """
        db_ret = db.session.query(MRole).all()
        ret = {}
        if db_ret is not None:
            for item in db_ret:
                ret[item.id] = item.name
        return ret

    @staticmethod
    def get_factory_id(db, id):
        """
        Get role name specified by id in m_role table
        :param db: Database object access
        :param id: role id
        :return: factory_id of factory
        """
        ret = db.session.query(MRole.factory_id).filter(MRole.id == id).first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def is_role_existing(db, id, factory_id=None):
        """
        Check if role is existing in m_role table
        :param db: Database object access
        :param factory_id: factory_id
        :return: true: existing, false: not existing
        """
        query = db.session.query(MRole.id).filter(MRole.id == id)
        if factory_id is not None:
            query = query.filter(MRole.factory_id == factory_id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def add(db, role):
        """
        Add role to m_role table
        :param db: DbAccess object (DbAccess)
        :param role: role info (m_role model)
        :return:
        """
        role.created = datetime.now()
        role.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(role)

    @staticmethod
    def update(db, role_id, role):
        """
        Edit role to m_role table (name, privilege_id only)
        :param db: DbAccess object (DbAccess)
        :param role_id: id role info(m_role model)
        :param role: role info(m_role model)
        :return:
        """
        db_role = db.session.query(MRole).filter_by(id=role_id).first()
        db_role.name = role.name
        db_role.privilege_id = role.privilege_id
        # auto update
        db_role.modified = datetime.now()
        db_role.upd_count = (db_role.upd_count + 1) if db_role.upd_count is not None else DbDefault.UPDATED_COUNT.value

    @staticmethod
    def delete(db, role_id):
        """
        delete role
        :param db: DbAccess object (DbAccess)
        :param role_id: id role info(m_role model)
        :return:
        """
        db.session.query(MRole).filter(MRole.id == role_id).delete()


# Class FunctionSql
class FunctionSql:
    @staticmethod
    def is_function_existing(db, id):
        """
        Check if role path is existing in m_role_function table
        :return: true: existing, false: not existing
        """
        ret = db.session.query(SFunction.id).filter(SFunction.id == id).first()
        return ret is not None


# Class LineSql
class LineSql:
    @staticmethod
    def get_line_list(db, factory_id=None):
        """
        Get list of all line in m_line table
        :return: [m_line]
        """
        cond = 1 == 1
        if factory_id is not None:
            cond = MLine.factory_id == factory_id
        ret = db.session.query(MLine).filter(cond).all()
        return ret

    @staticmethod
    def get_line(db, id):
        """
        Get line specified by id in m_line table
        :return: [m_line]
        """
        ret = db.session.query(MLine).filter(MLine.id == id).first()
        return ret

    @staticmethod
    def get_line_name(db, id):
        """
        Get line name specified by id in m_line table
        :param db: Database object access
        :param id: role id
        :return: line name (str)
        """
        ret = db.session.query(MLine.name).filter(MLine.id == id).first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def get_factory_id(db, id, factory_id=None):
        """
        Get factory id of line specified by id in m_line table
        :param db: Database object access
        :param id: line id
        :param factory_id: factory_id
        :return: factory_id
        """
        query = db.session.query(MLine.factory_id).filter(MLine.id == id)
        if factory_id is not None:
            query = query.filter(MLine.factory_id == factory_id)
        ret = query.first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def is_line_existing(db, id, factory_id=None):
        """
        Check if line is existing in m_line table
        :param db: Database object access
        :param id: line id
        :param factory_id: factory_id
        :return: true: existing, false: not existing
        """
        query = db.session.query(MLine.id).filter(MLine.id == id)
        if factory_id is not None:
            query = query.filter(MLine.factory_id == factory_id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def add(db, line):
        """
        Add line to m_line table
        :param db: DbAccess object (DbAccess)
        :param line: line info (m_line model)
        :return:
        """
        line.created = datetime.now()
        line.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(line)

    @staticmethod
    def update(db, line_id, line):
        """
        Edit line to m_line table
        :param db: DbAccess object (DbAccess)
        :param line_id: id line info(m_line model)
        :param line: line info(m_line model)
        :return:
        """
        db_line = db.session.query(MLine).filter_by(id=line_id).first()
        db_line.name = line.name
        # auto update
        db_line.modified = datetime.now()
        db_line.upd_count = (db_line.upd_count + 1) if db_line.upd_count is not None else DbDefault.UPDATED_COUNT.value

    @staticmethod
    def delete(db, line_id):
        """
        delete one line
        :param db: DbAccess object (DbAccess)
        :param line_id: id line info(m_line model)
        :return:
        """
        db.session.query(MLine).filter(MLine.id == line_id).delete()


# Class LineScannerSql
class LineScannerSql:
    @staticmethod
    def get_line_scanner_list(db, factory_id, line_id, scanner_id):
        """
        Get list of all line_scanner in m_line_scanner table
        :param db: Database object access
        :param factory_id: factory id
        :param line_id: line_id
        :param scanner_id: scanner_id
        :return: [MLineScanner]
        """
        query = db.session.query(MLineScanner)
        if factory_id is not None:
            query = query.filter(MLineScanner.factory_id == factory_id)
        if line_id is not None:
            query = query.filter(MLineScanner.line_id == line_id)
        if scanner_id is not None:
            query = query.filter(MLineScanner.scanner_id == scanner_id)
        ret = query.all()
        return ret

    @staticmethod
    def get_line_scanner(db, id):
        """
        Get line_scanner specified by id in m_line_scanner table
        :param d: line_scanner_id
        :return: [MLineScanner]
        """
        ret = db.session.query(MLineScanner).filter(MLineScanner.id == id).first()
        return ret

    @staticmethod
    def is_line_scanner_existing(db, id=None, line_id=None, scanner_id=None, factory_id=None):
        """
        Check if line_scanner is existing in m_line_scanner table
        :param id: line_scanner_id
        :param line_id: line_id
        :param scanner_id: scanner_id
        :param factory_id: factory_id
        :return: true: existing, false: not existing
        """
        query = db.session.query(MLineScanner.id)
        if id is not None:
            query = query.filter(MLineScanner.id == id)
        if line_id is not None:
            query = query.filter(MLineScanner.line_id == line_id)
        if scanner_id is not None:
            query = query.filter(MLineScanner.scanner_id == scanner_id)
        if factory_id is not None:
            query = query.filter(MLineScanner.factory_id == factory_id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def is_line_existing(db, id):
        """
        Check if line is existing in m_line_scanner table
        :param db: Database access object
        :param id: id
        :return: true: existing, false: not existing
        """
        ret = db.session.query(MLineScanner.line_id).filter(MLineScanner.line_id == id).first()
        return ret is not None

    @staticmethod
    def is_scanner_existing(db, id):
        """
        Check if scanner is existing in m_line_scanner table
        :param db: Database
        :param id: id
        :return: true: existing, false: not existing
        """
        ret = db.session.query(MLineScanner.scanner_id).filter(MLineScanner.scanner_id == id).first()
        return ret is not None

    @staticmethod
    def add(db, line_scanner):
        """
        Add line_scanner to m_line_scanner table
        :param db: DbAccess object (DbAccess)
        :param line_scanner: line scanner info (m_line_scanner model)
        :return:
        """
        line_scanner.created = datetime.now()
        line_scanner.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(line_scanner)

    @staticmethod
    def update(db, line_scanner_id, line_scanner):
        """
        Edit line_scanner to m_line_scanner table
        :param db: DbAccess object (DbAccess)
        :param line_scanner_id: id line scanner info(m_line_scanner model)
        :param line_scanner: line scanner info(m_line_scanner model)
        :return:
        """
        db_line_scanner = db.session.query(MLineScanner).filter_by(id=line_scanner_id).first()
        db_line_scanner.line_id = line_scanner.line_id
        db_line_scanner.scanner_id = line_scanner.scanner_id
        # auto update
        db_line_scanner.modified = datetime.now()
        db_line_scanner.upd_count = (db_line_scanner.upd_count + 1) if db_line_scanner.upd_count is not None else DbDefault.UPDATED_COUNT.value

    @staticmethod
    def delete(db, line_scanner_id):
        """
        Delete line_scanner from m_line_scanner table
        :param db: DbAccess object (DbAccess)
        :param line_scanner_id: id role path info(m_line_scanner model)
        :return:
        """
        db.session.query(MLineScanner).filter(MLineScanner.id == line_scanner_id).delete()


# Class MealSql
class MealSql:
    @staticmethod
    def get_meal_list(db, factory_id=None):
        """
        Get list of all meal in m_meal table
        :param db: Database access object
        :param factory_id: factory_id
        :return: [m_meal]
        """
        cond = 1 == 1
        if factory_id is not None:
            cond = MMeal.factory_id == factory_id
        ret = db.session.query(MMeal).filter(cond).all()
        return ret

    @staticmethod
    def get_meal(db, id):
        """
        Get Meal specified by id in m_meal table
        :param db: Database access object
        :param id: id
        :return: [m_meal]
        """
        ret = db.session.query(MMeal).filter(MMeal.id == id).first()
        return ret

    @staticmethod
    def get_meal_name(db, id):
        """
        Get Meal name specified by id in m_meal table
        :param db: Database access object
        :param id: meal_id
        :return: meal name (str)
        """
        ret = db.session.query(MMeal.name).filter(MMeal.id == id).first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def get_meal_name_dict(db, factory_id=None):
        """
        Get all meal name in m_meal table
        :param db: Database access object
        :param factory_id: factory_id
        :return: [m_meal]
        """
        cond = 1 == 1
        if factory_id is not None:
            cond = MMeal.factory_id == factory_id
        db_ret = db.session.query(MMeal).filter(cond).all()
        ret = {}
        if db_ret is not None:
            for item in db_ret:
                ret[item.id] = item.name
        return ret

    @staticmethod
    def is_meal_existing(db, id, factory_id=None):
        """
        Check if Meal is existing in m_meal table
        :param id: meal_id
        :param factory_id: factory_id
        :return: true: existing, false: not existing
        """
        query = db.session.query(MMeal.id).filter(MMeal.id == id)
        if factory_id is not None:
            query = query.filter(MMeal.factory_id == factory_id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def add(db, meal):
        """
        Add meal to m_meal table
        :param db: DbAccess object (DbAccess)
        :param meal: meal info (m_meal model)
        :return:
        """
        meal.created = datetime.now()
        meal.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(meal)

    @staticmethod
    def update(db, meal_id, meal):
        """
        Edit Meal to m_meal table
        :param db: DbAccess object (DbAccess)
        :param meal_id: id Meal info(m_meal model)
        :param meal: meal info(m_meal model)
        :return:
        """
        db_meal = db.session.query(MMeal).filter_by(id=meal_id).first()
        db_meal.name = meal.name
        # auto update
        db_meal.modified = datetime.now()
        db_meal.upd_count = (db_meal.upd_count + 1) if db_meal.upd_count is not None else DbDefault.UPDATED_COUNT.value

    @staticmethod
    def delete(db, meal_id):
        """
        delete one meal
        :param db: DbAccess object (DbAccess)
        :param meal_id: id meal info(m_meal model)
        :return:
        """
        db.session.query(MMeal).filter(MMeal.id == meal_id).delete()


# Class ScannerSql
class ScannerSql:
    @staticmethod
    def get_scanner_list(db, factory_id):
        """
        Get list of all scanner in m_scanner table
        :param db: Database access object
        :param factory_id: factory_id
        :return: [m_scanner]
        """
        cond = 1 == 1
        if factory_id is not None:
            cond = MScanner.factory_id == factory_id
        ret = db.session.query(MScanner).filter(cond).all()
        return ret

    @staticmethod
    def get_scanner(db, id):
        """
        Get scanner specified by id in m_scanner table
        :param db: Database access object
        :param id: scanner_id
        :return: [m_scanner]
        """
        ret = db.session.query(MScanner).filter(MScanner.id == id).first()
        return ret

    @staticmethod
    def get_scanner_name(db, id):
        """
        Get scanner name specified by id in m_scanner table
        :param db: Database access object
        :param id: scanner_id
        :return: scanner name (str)
        """
        ret = db.session.query(MScanner.name).filter(MScanner.id == id).first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def get_factory_id(db, id, factory_id=None):
        """
        Get factory_id of scanner specified by id in m_scanner table
        :param db: Database access object
        :param factory_id: factory_id
        :return: true: existing, false: not existing
        """
        query = db.session.query(MScanner.factory_id).filter(MScanner.id == id)
        if factory_id is not None:
            query = query.filter(MScanner.factory_id == factory_id)
        ret = query.first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def is_scanner_existing(db, id, factory_id=None):
        """
        Check if scanner is existing in m_scanner table
        :param db: Database access object
        :param id: scanner_id
        :param factory_id: factory_id
        :return: true: existing, false: not existing
        """
        query = db.session.query(MScanner.id).filter(MScanner.id == id)
        if factory_id is not None:
            query = query.filter(MScanner.factory_id == factory_id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def add(db, scanner):
        """
        Add scanner to m_scanner table
        :param db: DbAccess object (DbAccess)
        :param scanner: scanner info (m_scanner model)
        :return:
        """
        scanner.created = datetime.now()
        scanner.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(scanner)

    @staticmethod
    def update(db, scanner_id, scanner):
        """
        Edit scanner to m_scanner table
        :param db: DbAccess object (DbAccess)
        :param scanner_id: id scanner info(m_scanner model)
        :param scanner: scanner info(m_scanner model)
        :return:
        """
        db_scanner = db.session.query(MScanner).filter_by(id=scanner_id).first()
        db_scanner.name = scanner.name
        db_scanner.ip_address = scanner.ip_address
        # auto update
        db_scanner.modified = datetime.now()
        db_scanner.upd_count = (db_scanner.upd_count + 1) if db_scanner.upd_count is not None else DbDefault.UPDATED_COUNT.value

    @staticmethod
    def delete(db, scanner_id):
        """
        delete one scanner
        :param db: DbAccess object (DbAccess)
        :param scanner_id: id scanner info(m_scanner model)
        :return:
        """
        db.session.query(MScanner).filter(MScanner.id == scanner_id).delete()


# Class ShiftMealSql
class ShiftMealSql:
    @staticmethod
    def get_shift_meal_list(db, shift_id=None, meal_id=None, factory_id=None, sort_request=False):
        """
        Get ShiftMeal list from m_shift_meal table
        :return: [MShiftMeal]
        """
        query = db.session.query(MShiftMeal)
        if shift_id is not None:
            query = query.filter(MShiftMeal.shift_id == shift_id)
        if meal_id is not None:
            query = query.filter(MShiftMeal.meal_id == meal_id)
        if factory_id is not None:
            query = query.filter(MShiftMeal.factory_id == factory_id)
        if sort_request:
            query = query.order_by(MShiftMeal.serving_day_after_register)
        ret = query.all()
        return ret

    @staticmethod
    def get_multi_shift_meal_list(db, shift_list=None, factory_id=None, sort_request=False):
        """
        Get ShiftMeal list from m_shift_meal table
        :return: [MShiftMeal]
        """
        query = db.session.query(MShiftMeal)
        if shift_list is not None:
            query = query.filter(MShiftMeal.shift_id.in_(shift_list))
        if factory_id is not None:
            query = query.filter(MShiftMeal.factory_id == factory_id)
        if sort_request:
            query = query.order_by(MShiftMeal.serving_day_after_register)
        ret = query.all()
        return ret

    @staticmethod
    def get_shift_meal_list_by_factory_id(db, factory_id):
        """
        get shift meal list filtered by factory_id from m_shift_meal table
        :param db:
        :param factory_id:
        :return:  [MShiftMeal]
        """
        query = db.session.query(MShiftMeal)
        if factory_id is not None:
            query = query.filter(MShiftMeal.factory_id == factory_id)
        ret = query.all()
        return ret

    @staticmethod
    def get_shift_meal_name(db, id):
        """
        Get ShiftMeal list from m_shift_meal table
        :param id: shift_meal_id
        :return: shift meal name (str)
        """
        query = db.session.query(MShiftMeal.name)
        if id is not None:
            query = query.filter(MShiftMeal.id == id)
        ret = query.first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def get_shift_meal_name_dict(db, factory_id=None):
        """
        Get ShiftMeal list from m_shift_meal table
        :return: shift meal name (str)
        """
        query = db.session.query(MShiftMeal)
        if factory_id is not None:
            query = query.filter(MShiftMeal.factory_id == factory_id)
        db_ret = query.all()
        ret = {}
        if db_ret is not None:
            for item in db_ret:
                ret[item.id] = item.name
        return ret

    @staticmethod
    def get_shift_meal(db, id=None, shift_id=None, meal_id=None, factory_id=None):
        """
        Get shift meal from m_shift_meal table
        :param id: shift_meal_id
        :return: shift meal (MShiftMeal)
        """
        query = db.session.query(MShiftMeal)
        if id is not None:
            query = query.filter(MShiftMeal.id == id)
        if shift_id is not None:
            query = query.filter(MShiftMeal.shift_id == shift_id)
        if meal_id is not None:
            query = query.filter(MShiftMeal.meal_id == meal_id)
        if factory_id is not None:
            query = query.filter(MShiftMeal.factory_id == factory_id)
        ret = query.first()
        return ret

    @staticmethod
    def is_meal_existing(db, id):
        """
        Check if meal is existing in m_shift_meal table
        :param id: meal_id
        :return: true: existing, false: not existing
        """
        ret = db.session.query(MShiftMeal.meal_id).filter(MShiftMeal.meal_id == id).first()
        return ret is not None

    @staticmethod
    def is_shift_existing(db, id):
        """
        Check if shift is existing in m_shift_meal table
        :param id: shift_id
        :return: true: existing, false: not existing
        """
        ret = db.session.query(MShiftMeal.shift_id).filter(MShiftMeal.shift_id == id).first()
        return ret is not None

    @staticmethod
    def is_shift_meal_existing(db, id=None, shift_id=None, meal_id=None, factory_id=None):
        """
        Check if meal, shift is existing in m_shift_meal table
        :param id: shift_id
        :return: true: existing, false: not existing
        """
        query = db.session.query(MShiftMeal.id)
        if id is not None:
            query = query.filter(MShiftMeal.id == id)
        if shift_id is not None:
            query = query.filter(MShiftMeal.shift_id == shift_id)
        if meal_id is not None:
            query = query.filter(MShiftMeal.meal_id == meal_id)
        if factory_id is not None:
            query = query.filter(MShiftMeal.factory_id == factory_id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def add(db, shift_meal):
        """
        Add shift_meal to m_shift_meal table
        :param db: DbAccess object (DbAccess)
        :param shift_meal: shift_meal info (m_shift_meal model)
        :return:
        """
        shift_meal.created = datetime.now()
        shift_meal.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(shift_meal)

    @staticmethod
    def update(db, shift_meal_id, shift_meal):
        """
        Edit shift_meal to m_shift_meal table
        :param db: DbAccess object (DbAccess)
        :param shift_meal_id: shift_meal id
        :param shift_meal: shift_meal info(m_scanner model)
        :return:
        """
        db_shift_meal = db.session.query(MShiftMeal).filter_by(id=shift_meal_id).first()
        db_shift_meal.name = shift_meal.name
        db_shift_meal.shift_id = shift_meal.shift_id
        db_shift_meal.meal_id = shift_meal.meal_id
        db_shift_meal.start_register = shift_meal.start_register
        db_shift_meal.end_register = shift_meal.end_register
        db_shift_meal.start_serving = shift_meal.start_serving
        db_shift_meal.end_serving = shift_meal.end_serving
        db_shift_meal.serving_day_after_register = shift_meal.serving_day_after_register
        db_shift_meal.overtime = shift_meal.overtime
        db_shift_meal.register_until_today_plus = shift_meal.register_until_today_plus
        db_shift_meal.default_serving_id = shift_meal.default_serving_id
        # auto update
        db_shift_meal.modified = datetime.now()
        db_shift_meal.upd_count = (db_shift_meal.upd_count + 1) if db_shift_meal.upd_count is not None else DbDefault.UPDATED_COUNT.value

    @staticmethod
    def delete(db, shift_meal_id):
        """
        Delete shift_meal from m_shift_meal table
        :param db: DbAccess object (DbAccess)
        :param shift_meal_id: id scanner info(m_scanner model)
        :return:
        """
        db.session.query(MShiftMeal).filter(MShiftMeal.id == shift_meal_id).delete()

    @staticmethod
    def is_shift_meal_in_time (db, current_time):
        """
        Delete shift_meal from m_shift_meal table
        :return:
        """
        query = db.session.query(MShiftMeal).filter(current_time >= MShiftMeal.start_register, current_time <= MShiftMeal.end_register)
        ret = query.first()
        return ret


class TSessionSql:
    @staticmethod
    def get_session(db, user_id):
        """
        Get session info by specified user id
        :param db: Database access object
        :type db: DbAccess
        :param user_id: user id
        :type user_id: int
        :return: SSession of specified ser id, None if not exist
        :rtype: TSession
        """
        session = db.session.query(TSession) \
            .filter(TSession.user_id == user_id) \
            .first()
        if session is None:
            return None
        return session

    @staticmethod
    def get_session_by_key(db, session_key):
        """
        Get session info by specified session key
        :param db: Database access object
        :type db: DbAccess
        :param session_key: session_key
        :type session_key: int
        :return: SSession of specified session key, None if not exist
        :rtype: TSession
        """
        session = db.session.query(TSession) \
            .filter(TSession.key == session_key) \
            .first()
        if session is None:
            return None
        return session

    @staticmethod
    def delete_expired_key(db):
        """
        Delete all expired session
        :param db: Database access object
        :type db: DbAccess
        :return: -
        :rtype: -
        """
        db.session.query(TSession) \
            .filter(TSession.expired < datetime.now()) \
            .delete()


class ShiftMealServingSql:
    @staticmethod
    def getlist_by_shift_meal_id(db, shift_meal_id, serving_id):
        """
        get list of MShiftMealServing by shift_meal_id, serving_id
        :param db:
        :param shift_meal_id: int
        :param serving_id: int
        :return: [MShiftMealServing]
        """
        query = db.session.query(MShiftMealServing)\
            .join(MServing, MServing.id == MShiftMealServing.serving_id)\
            .filter(MShiftMealServing.shift_meal_id == shift_meal_id)
        if serving_id is not None:
            query = query.filter(MShiftMealServing.serving_id == serving_id)
        return query.all()

    @staticmethod
    def get_list_by_serving_id(db, serving_id=None):
        """
        get list of MShiftMealServing by shift_meal_id, serving_id
        :param db:
        :param serving_id: int
        :return: [MShiftMealServing]
        """
        query = db.session.query(MShiftMealServing)
        if serving_id is not None:
            query = query.filter(MShiftMealServing.serving_id == serving_id)
        return query.all()

    @staticmethod
    def get_shift_meal_id_list(db, factory_id, shiftmeal_id, serving_id):
        """
        Get list of all ShiftMealServing in m_shift_meal_serving table
        :return: MShiftMealServing
        :rtype: list
        """
        query = db.session.query(MShiftMealServing.shift_meal_id)\
            .join(MShiftMeal, MShiftMeal.id == MShiftMealServing.shift_meal_id)\
            .join(MMeal, MMeal.id == MShiftMeal.meal_id)
        if factory_id is not None:
            query = query.filter(MMeal.factory_id == factory_id)
        if shiftmeal_id is not None:
            query = query.filter(MShiftMeal.id == shiftmeal_id)
        if serving_id is not None:
            query = query.filter(MShiftMealServing.serving_id == serving_id)
        ret = query.group_by(MShiftMealServing.shift_meal_id).all()
        if ret is None:
            return[]
        return [val[0] for val in ret]

    @staticmethod
    def get_shift_meal_serving(db, id):
        """
        Get shift_meal_serving specified by id in m_shift_meal_serving table
        :return: MShiftMealServing
        """
        ret = db.session.query(MShiftMealServing).filter(MShiftMealServing.id == id).first()
        return ret

    @staticmethod
    def get_shift_meal_serving_by_factory_id(db, factory_id):
        """
        Get shift meal serving list by factory id in shift_meal_serving table
        :param db:
        :param factory_id:
        :return: [MShiftMealServing]
        """
        query = db.session.query(MShiftMealServing)
        if factory_id is not None:
            query = query.filter(MShiftMealServing.factory_id == factory_id)
        return query.all()

    @staticmethod
    def get_shift_meal_serving_by_shift_id(db, id):
        """
        :param db:
        :param id:
        :return:
        """
        ret = db.session.query(MShiftMealServing)\
              .join(MShiftMeal, MShiftMealServing.shift_meal_id == MShiftMeal.id)\
              .filter(MShiftMeal.shift_id == id)\
              .all()
        return ret

    @staticmethod
    def is_shift_meal_serving_existing(db, id=None, shift_meal_id=None, serving_id=None, factory_id=None):
        """
        :param db:
        :param id: int
        :param shift_meal_id:int
        :param serving_id: int
        :param factory_id: int
        :return: true if existing, false if not existing
        """
        query = db.session.query(MShiftMealServing)
        if id is not None:
            query = query.filter(MShiftMealServing.id == id)
        if shift_meal_id is not None:
            query = query.filter(MShiftMealServing.shift_meal_id == shift_meal_id)
        if serving_id is not None:
            query = query.filter(MShiftMealServing.serving_id == serving_id)
        if factory_id is not None:
            query = query.filter(MShiftMealServing.factory_id == factory_id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def is_serving_existing(db, id):
        """
        :param db:
        :param id: int
        :return: true if existing, false if not existing
        """
        ret = db.session.query(MShiftMealServing.serving_id).filter(MShiftMealServing.serving_id == id).first()
        return ret is not None

    @staticmethod
    def add(db, shift_meal_serving):
        """
        Add shift_meal_serving to m_shift_meal_serving table
        :return:
        """
        shift_meal_serving.created = datetime.now()
        shift_meal_serving.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(shift_meal_serving)

    @staticmethod
    def update(db, shift_meal_serving_id, shift_meal_serving):
        """
        Edit line to m_shift_meal_serving table
        :return:
        """
        db_sm_serving = db.session.query(MShiftMealServing).filter_by(id=shift_meal_serving_id).first()
        db_sm_serving.shift_meal_id = shift_meal_serving.shift_meal_id
        db_sm_serving.serving_id = shift_meal_serving.serving_id
        # auto update
        db_sm_serving.modified = datetime.now()
        db_sm_serving.upd_count = (
                    db_sm_serving.upd_count + 1) if db_sm_serving.upd_count is not None else DbDefault.UPDATED_COUNT.value

    @staticmethod
    def delete(db, shift_meal_serving_id):
        """
        Delete one shift meal serving from m_shift_meal_serving table
        :return:
        """
        db.session.query(MShiftMealServing).filter(MShiftMealServing.id == shift_meal_serving_id).delete()

    @staticmethod
    def is_shift_meal_existing(db, id):
        """
        Check if shift_meal is existing in m_shift_meal table
        :return: true: existing, false: not existing
        """
        ret = db.session.query(MShiftMealServing.shift_meal_id).filter(MShiftMealServing.shift_meal_id == id).first()
        return ret is not None

    @staticmethod
    def get_shift_meal_serving_name(db, id):
        """
        :param db:
        :param id: int
        :return: name of MShiftMealServing
        """
        query = db.session.query(MShiftMealServing.name)
        if id is not None:
            query = query.filter(MShiftMealServing.id == id)
        ret = query.first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def get_shift_meal_serving_served_list_by_line_id(db, id=None, line_id=None):
        """
        :param db:
        :param id: int
        :param line_id: int
        :return:
        """
        query = db.session.query(MShiftMealServing)\
            .join(MLineShiftMealServing, MShiftMealServing.id == MLineShiftMealServing.shift_meal_serving_id)
        if id is not None:
            query = query.filter(MLineShiftMealServing.id != id)
        if line_id is not None:
            query = query.filter(MLineShiftMealServing.line_id == line_id)
        ret = query.all()
        return ret

    @staticmethod
    def is_shift_meal_serving_by_shift_meal_id_serving_id_factory_id(db, shift_meal_id, serving_id, factory_id):
        """
        :param db:
        :param shift_meal_id:
        :param serving_id:
        :param factory_id:
        :return:
        """
        ret = db.session.query(MShiftMealServing)\
              .filter(MShiftMealServing.shift_meal_id == shift_meal_id, MShiftMealServing.serving_id == serving_id,
                      MShiftMealServing.factory_id == factory_id)\
              .first()
        return ret is not None


class GroupLineShiftMealServingSql:
    @staticmethod
    def get_shift_meal_serving_by_factory_id(db, factory_id=None):
        """
        get list of MGroupLineShiftMealServing by factory_id
        :param db:
        :param factory_id: int
        :return: [MGroupLineShiftMealServing]
        """
        query = db.session.query(MGroupLineShiftMealServing)
        if factory_id is not None:
            query = query.filter(MGroupLineShiftMealServing.factory_id == factory_id)
        return query.all()

    @staticmethod
    def is_group_line_shift_meal_existing(db, group_line_id, factory_id=None):
        """
        Check if shift is existing in m_shift table
        :return: true: existing, false: not existing
        """
        query = db.session.query(MGroupLineShiftMealServing).filter(MGroupLineShiftMealServing.id == group_line_id)
        if factory_id is not None:
            query = query.filter(MGroupLineShiftMealServing.factory_id == factory_id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def delete(db, group_line_id):
        """
        delete user
        :param db: DbAccess object (DbAccess)
        :param group_line_id: id user info(m_user model)
        :return:
        """
        db.session.query(MGroupLineShiftMealServing).filter(MGroupLineShiftMealServing.id == group_line_id).delete()

    @staticmethod
    def update(db, group_line_id, group_line_shift_meal_serving):
        """
        Edit group_line_shift_meal_serving to m_group_line_shift_meal_serving table
        :param db: DbAccess object (DbAccess)
        :param group_line_id: id group line shift meal serving(m_group_line_shift_meal_serving model)
        :param group_line_shift_meal_serving: group line shift meal serving info(m_group_line_shift_meal_serving model)
        :return:
        """
        db_line = db.session.query(MGroupLineShiftMealServing).filter_by(id=group_line_id).first()
        db_line.factory_id = group_line_shift_meal_serving.factory_id
        db_line.name = group_line_shift_meal_serving.name
        db_line.start_serving = group_line_shift_meal_serving.start_serving
        db_line.end_serving = group_line_shift_meal_serving.end_serving
        # auto update
        db_line.modified = datetime.now()
        db_line.upd_count = (db_line.upd_count + 1) if db_line.upd_count is not None else DbDefault.UPDATED_COUNT.value

    @staticmethod
    def add(db, group_line_shift_meal_serving):
        """
        :param db:
        :param group_line_shift_meal_serving:
        :return:
        """
        group_line_shift_meal_serving.created = datetime.now()
        db.session.add(group_line_shift_meal_serving)

    @staticmethod
    def get_group_name(db, group_line_id):
        ret = db.session.query(MGroupLineShiftMealServing).filter_by(id=group_line_id).first()
        if ret is not None:
            return ret.name

    @staticmethod
    def get_group_line_served_list(db, group_line_id=None, factory_id=None):
        """
        get list of MGroupLineShiftMealServing by factory_id
        :param db:
        :param group_line_id: int
        :param factory_id: int
        :return: [MGroupLineShiftMealServing]
        """
        query = db.session.query(MGroupLineShiftMealServing)
        if factory_id is not None:
            query = query.filter(MGroupLineShiftMealServing.factory_id == factory_id)
        if group_line_id is not None:
            query = query.filter(MGroupLineShiftMealServing.id == group_line_id)
        return query.all()


class ServingSql:
    @staticmethod
    def get_serving_name(db, id):
        """
        Get serving name in m_serving table
        :return: serving name (str)
        """
        ret = db.session.query(MServing.name).filter(MServing.id == id).first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def get_serving_name_dict(db, factory_id=None):
        """
        Get all serving name
        :return: serving name dict {id: name}
        """
        query = db.session.query(MServing)
        if factory_id is not None:
            query = query.filter(MServing.factory_id == factory_id)
        db_ret = query.all()
        ret = {}
        if db_ret is not None:
            for item in db_ret:
                ret[item.id] = item.name
        return ret

    @staticmethod
    def is_serving_existing(db, id, factory_id=None, out_of_service=None):
        """
        Check if serving is existing in m_serving table
        :return: true: existing, false: not existing
        """
        query = db.session.query(MServing).filter(MServing.id == id)
        if factory_id is not None:
            query = query.filter(MServing.factory_id == factory_id)
        if out_of_service is not None:
            query = query.filter(MServing.out_of_service == out_of_service)
        ret = query.first()
        return ret is not None

    @staticmethod
    def getlist_by_shiftmeal_id(db, shiftmeal_id):
        """
        :param db:
        :param shift meal_id:
        :return:
        """
        ret = db.session.query(MServing)\
            .join(MShiftMealServing, MServing.id == MShiftMealServing.serving_id)\
            .filter(MShiftMealServing.shift_meal_id == shiftmeal_id)
        return ret

    @staticmethod
    def get_serving_list(db, out_of_service=None, factory_id=None):
        """
        :param db:
        :param out_of_service:
        :param factory_id:
        :return: [MServing]
        """
        query = db.session.query(MServing)
        if out_of_service is not None:
            query = query.filter(MServing.out_of_service == out_of_service)
        if factory_id is not None:
            query = query.filter(MServing.factory_id == factory_id)
        ret = query.all()
        return ret

    @staticmethod
    def add(db, serving):
        """
        :param db:
        :param serving:
        :return:
        """
        serving.created = datetime.now()
        serving.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(serving)

    @staticmethod
    def update(db, id, serving):
        """
        :param db:
        :param id:
        :param serving:
        :return:
        """
        db_serving = db.session.query(MServing).filter(MServing.id == id).first()
        db_serving.name = serving.name
        db_serving.name_en = serving.name_en
        # Auto update
        db_serving.modified = datetime.now()
        db_serving.upd_count = (db_serving.upd_count + 1) if db_serving.upd_count is not None else DbDefault.UPDATED_COUNT.value

    @staticmethod
    def delete(db, id):
        """
        :param db:
        :param id:
        :return:
        """
        serving = db.session.query(MServing).filter(MServing.id == id).first()
        serving.out_of_service = 1


class StaffServingSql:

    # get list of served shift from db filter to now and factory_id
    @staticmethod
    def get_server_shift_list(db, date, factory_id):
        ret = db.session.query(TStaffServing.shift_id)\
              .filter(TStaffServing.served_date == date, TStaffServing.factory_id == factory_id)\
              .group_by(TStaffServing.shift_id)\
              .all()
        if ret is None:
            return []
        return [val[0] for val in ret]

    # get list of serving_id from db to filter shift_id,  date
    @staticmethod
    def get_staff_serving_list_by_shift_and_line(db, date, shift_id_list, line_id_list):
        """
        :param db:
        :param date:
        :param shift_id:
        :param line_id_list:
        :return:
        """
        ret = db.session.query(TStaffServing.shift_id, TStaffServing.line_id, TStaffServing.serving_id, func.count(TStaffServing.staff_id).label('total'))\
              .filter(TStaffServing.served_date == date, TStaffServing.shift_id.in_(shift_id_list), TStaffServing.line_id.in_(line_id_list))\
              .group_by(TStaffServing.shift_id, TStaffServing.line_id, TStaffServing.serving_id)\
              .order_by(TStaffServing.line_id)\
              .all()
        return ret

    @staticmethod
    def get_staff_serving_list(db, staff_serving, department_id_list):
        """
        get list of staff serving filtered by factory id, staff id, shift_id, meal_id, serving_id, start_date, end_date, month
        """
        list_staff_id = None
        if department_id_list is not None:
            list_staff_id = StaffSql.get_staff_id_all_filter_by_department_list(db, department_id_list)
        # make query
        query = db.session.query(TStaffServing)
        if staff_serving.factory_id is not None:
            query = query.filter(TStaffServing.factory_id == staff_serving.factory_id)
        if staff_serving.staff_id is not None:
            query = query.filter(TStaffServing.staff_id == staff_serving.staff_id)
        if staff_serving.shift_id is not None:
            query = query.filter(TStaffServing.shift_id == staff_serving.shift_id)
        if staff_serving.meal_id is not None:
            query = query.filter(TStaffServing.meal_id == staff_serving.meal_id)
        if staff_serving.serving_id is not None:
            query = query.filter(TStaffServing.serving_id == staff_serving.serving_id)
        if staff_serving.start_date is not None and staff_serving.end_date is not None:
            query = query.filter(TStaffServing.served_date >= staff_serving.start_date,
                                 TStaffServing.served_date <= staff_serving.end_date)
        if staff_serving.month is not None:
            from smartcanteen.util.common import Util
            start_date, end_date = Util.get_month_range(staff_serving.month)
            query = query.filter(TStaffServing.served_date >= start_date,
                                 TStaffServing.served_date <= end_date)

        if list_staff_id is None or len(list_staff_id) == 0:
            ret = query.all()
        else:
            # because of pyodbc LIMITATION, prevent query over 2100 parameter
            ret = exec_query_get_list(query, TStaffServing.staff_id, list_staff_id)
        return ret

    @staticmethod
    def get_staff_report_list(db, report_filter, department_id_list=None):
        """
        get list of staff serving filtered by factory id, staff id, shift_id, meal_id, serving_id, start_date, end_date, month
        """
        list_staff_id = None
        if department_id_list is not None:
            list_staff_id = StaffSql.get_staff_id_all_filter_by_department_list(db, department_id_list)
        # make query
        query = db.session.query(TStaffServing.staff_id, TStaffServing.staff_name,
                                 TStaffServing.serving_id, func.count(TStaffServing.serving_id))
        if report_filter.factory_id is not None:
            query = query.filter(TStaffServing.factory_id == report_filter.factory_id)
        if report_filter.staff_id is not None:
            query = query.filter(TStaffServing.staff_id == report_filter.staff_id)
        if report_filter.shift_id is not None:
            query = query.filter(TStaffServing.shift_id == report_filter.shift_id)
        if report_filter.meal_id is not None:
            query = query.filter(TStaffServing.meal_id == report_filter.meal_id)
        if report_filter.serving_id is not None:
            query = query.filter(TStaffServing.serving_id == report_filter.serving_id)
        if report_filter.start_date is not None and report_filter.end_date is not None:
            query = query.filter(TStaffServing.served_date >= report_filter.start_date,
                                 TStaffServing.served_date <= report_filter.end_date)
        if report_filter.month is not None:
            from smartcanteen.util.common import Util
            start_date, end_date = Util.get_month_range(report_filter.month)
            query = query.filter(TStaffServing.served_date >= start_date,
                                 TStaffServing.served_date <= end_date)
        query = query.group_by(TStaffServing.staff_id, TStaffServing.staff_name, TStaffServing.serving_id)

        if list_staff_id is None or len(list_staff_id) == 0:
            ret = query.all()
        else:
            # because of pyodbc LIMITATION, prevent query over 2100 parameter
            ret = exec_query_get_list(query, TStaffServing.staff_id, list_staff_id)
        return ret

    @staticmethod
    def get_dept_report_list(db, report_filter):
        """
        get list of staff serving filtered by factory id, staff id, shift_id, meal_id, serving_id, start_date, end_date, month
        """
        list_staff_id = None
        if report_filter.department_id is not None:
            list_staff_id = StaffSql.get_staff_id_all(db, report_filter.department_id)
        # make query
        query = db.session.query(TDepartment.id, TDepartment.name,
                                 TStaffServing.serving_id, func.count(TStaffServing.serving_id))\
            .join(TStaffServing, TDepartment.id == TStaffServing.department_id)
        if report_filter.factory_id is not None:
            query = query.filter(TStaffServing.factory_id == report_filter.factory_id)
        if report_filter.staff_id is not None:
            query = query.filter(TStaffServing.staff_id == report_filter.staff_id)
        if report_filter.shift_id is not None:
            query = query.filter(TStaffServing.shift_id == report_filter.shift_id)
        if report_filter.meal_id is not None:
            query = query.filter(TStaffServing.meal_id == report_filter.meal_id)
        if report_filter.serving_id is not None:
            query = query.filter(TStaffServing.serving_id == report_filter.serving_id)
        if report_filter.start_date is not None and report_filter.end_date is not None:
            query = query.filter(TStaffServing.served_date >= report_filter.start_date,
                                 TStaffServing.served_date <= report_filter.end_date)
        if report_filter.month is not None:
            from smartcanteen.util.common import Util
            start_date, end_date = Util.get_month_range(report_filter.month)
            query = query.filter(TStaffServing.served_date >= start_date,
                                 TStaffServing.served_date <= end_date)
        query = query.group_by(TDepartment.id, TDepartment.name, TStaffServing.serving_id)

        if list_staff_id is None or len(list_staff_id) == 0:
            ret = query.all()
        else:
            # because of pyodbc LIMITATION, prevent query over 2100 parameter
            ret = exec_query_get_list(query, TStaffServing.staff_id, list_staff_id)
        return ret

    @staticmethod
    def get_export_dept_report_list(db, report_filter, dept_list=None):
        """
        get list of staff serving filtered by factory id, staff id, shift_id, meal_id, serving_id, start_date, end_date, month
        """
        list_staff_id = None
        if dept_list is not None:
            list_staff_id = StaffSql.get_staff_id_all_filter_by_department_list(db, dept_list)
        # make query
        query = db.session.query(TStaffServing.served_date, TDepartment.id,
                                 TStaffServing.meal_id, TStaffServing.serving_id,
                                 func.count(TStaffServing.staff_id).label('total'))\
            .join(TStaffServing, TDepartment.id == TStaffServing.department_id)

        if report_filter.factory_id is not None:
            query = query.filter(TStaffServing.factory_id == report_filter.factory_id)
        if report_filter.staff_id is not None:
            query = query.filter(TStaffServing.staff_id == report_filter.staff_id)
        if report_filter.shift_id is not None:
            query = query.filter(TStaffServing.shift_id == report_filter.shift_id)
        if report_filter.meal_id is not None:
            query = query.filter(TStaffServing.meal_id == report_filter.meal_id)
        if report_filter.serving_id is not None:
            query = query.filter(TStaffServing.serving_id == report_filter.serving_id)
        if report_filter.start_date is not None and report_filter.end_date is not None:
            query = query.filter(TStaffServing.served_date >= report_filter.start_date,
                                 TStaffServing.served_date <= report_filter.end_date)
        if report_filter.month is not None:
            from smartcanteen.util.common import Util
            start_date, end_date = Util.get_month_range(report_filter.month)
            query = query.filter(TStaffServing.served_date >= start_date,
                                 TStaffServing.served_date <= end_date)

        query = query.group_by(TStaffServing.served_date, TDepartment.id,
                               TStaffServing.meal_id, TStaffServing.serving_id) \
            .order_by(TStaffServing.served_date)

        if list_staff_id is None or len(list_staff_id) == 0:
            ret = query.all()
        else:
            # because of pyodbc LIMITATION, prevent query over 2100 parameter
            ret = exec_query_get_list(query, TStaffServing.staff_id, list_staff_id)
        return ret

    @staticmethod
    def get_serving_report_list(db, report_filter, department_id_list=None):
        """
        get list of staff serving filtered by factory id, staff id, shift_id, meal_id, serving_id, start_date, end_date, month
        """
        list_staff_id = None
        if department_id_list is not None:
            list_staff_id = StaffSql.get_staff_id_all_filter_by_department_list(db, department_id_list)
        # make query
        query = db.session.query(TStaffServing.serving_id, func.count(TStaffServing.staff_id))
        if report_filter.factory_id is not None:
            query = query.filter(TStaffServing.factory_id == report_filter.factory_id)
        if report_filter.staff_id is not None:
            query = query.filter(TStaffServing.staff_id == report_filter.staff_id)
        if report_filter.shift_id is not None:
            query = query.filter(TStaffServing.shift_id == report_filter.shift_id)
        if report_filter.meal_id is not None:
            query = query.filter(TStaffServing.meal_id == report_filter.meal_id)
        if report_filter.serving_id is not None:
            query = query.filter(TStaffServing.serving_id == report_filter.serving_id)
        if report_filter.start_date is not None and report_filter.end_date is not None:
            query = query.filter(TStaffServing.served_date >= report_filter.start_date,
                                 TStaffServing.served_date <= report_filter.end_date)
        if report_filter.month is not None:
            from smartcanteen.util.common import Util
            start_date, end_date = Util.get_month_range(report_filter.month)
            query = query.filter(TStaffServing.served_date >= start_date,
                                 TStaffServing.served_date <= end_date)
        query = query.group_by(TStaffServing.serving_id).order_by(TStaffServing.serving_id)

        if list_staff_id is None or len(list_staff_id) == 0:
            ret = query.all()
        else:
            # because of pyodbc LIMITATION, prevent query over 2100 parameter
            ret = exec_query_get_list(query, TStaffServing.staff_id, list_staff_id)
        return ret

    @staticmethod
    def get_dept_staff_served_report_list(db, report_filter, department_id_list=None):
        """
        get list of staff register filtered by factory id, staff id,
        shift_id, meal_id, serving_id, start_date, end_date, month
        """
        list_staff_id = None
        if department_id_list is not None:
            list_staff_id = StaffSql.get_staff_id_all_filter_by_department_list(db, department_id_list)

        # make query
        query = db.session.query(TDepartment.id, TDepartment.name, TStaffServing.meal_id,
                                 TStaffServing.serving_id, func.count(TStaffServing.id).label('total')) \
            .join(TStaffServing, TDepartment.id == TStaffServing.department_id)

        if report_filter.factory_id is not None:
            query = query.filter(TStaffServing.factory_id == report_filter.factory_id)
        if report_filter.staff_id is not None:
            query = query.filter(TStaffServing.staff_id == report_filter.staff_id)
        if report_filter.shift_id is not None:
            query = query.filter(TStaffServing.shift_id == report_filter.shift_id)
        if report_filter.meal_id is not None:
            query = query.filter(TStaffServing.meal_id == report_filter.meal_id)
        if report_filter.serving_id is not None:
            query = query.filter(TStaffServing.serving_id == report_filter.serving_id)
        if report_filter.start_date is not None and report_filter.end_date is not None:
            query = query.filter(TStaffServing.served_date >= report_filter.start_date,
                                 TStaffServing.served_date <= report_filter.end_date)
        if report_filter.month is not None:
            from smartcanteen.util.common import Util
            start_date, end_date = Util.get_month_range(report_filter.month)
            query = query.filter(TStaffServing.served_date >= start_date,
                                 TStaffServing.served_date <= end_date)

        query = query.group_by(TDepartment.id, TDepartment.name,
                               TStaffServing.meal_id, TStaffServing.serving_id)

        if list_staff_id is None or len(list_staff_id) == 0:
            ret = query.all()
        else:
            # because of pyodbc LIMITATION, prevent query over 2100 parameter
            ret = exec_query_get_list(query, TStaffServing.staff_id, list_staff_id)
        return ret

    @staticmethod
    def get_kitchen_report_list(db, report_filter, department_id_list=None):
        """
        get list of staff serving filtered by factory id, staff id, shift_id, meal_id, serving_id, start_date, end_date, month
        """
        list_staff_id = None
        if department_id_list is not None:
            list_staff_id = StaffSql.get_staff_id_all_filter_by_department_list(db, department_id_list)
        # make query
        query = db.session.query(TStaffServing.served_date, TStaffServing.shift_id, TStaffServing.meal_id, TStaffServing.serving_id,
                                 func.count(TStaffServing.staff_id).label('total'))
        if report_filter.factory_id is not None:
            query = query.filter(TStaffServing.factory_id == report_filter.factory_id)
        if report_filter.staff_id is not None:
            query = query.filter(TStaffServing.staff_id == report_filter.staff_id)
        if report_filter.shift_id is not None:
            query = query.filter(TStaffServing.shift_id == report_filter.shift_id)
        if report_filter.meal_id is not None:
            query = query.filter(TStaffServing.meal_id == report_filter.meal_id)
        if report_filter.serving_id is not None:
            query = query.filter(TStaffServing.serving_id == report_filter.serving_id)
        if report_filter.start_date is not None and report_filter.end_date is not None:
            query = query.filter(TStaffServing.served_date >= report_filter.start_date,
                                 TStaffServing.served_date <= report_filter.end_date)
        if report_filter.month is not None:
            from smartcanteen.util.common import Util
            start_date, end_date = Util.get_month_range(report_filter.month)
            query = query.filter(TStaffServing.served_date >= start_date,
                                 TStaffServing.served_date <= end_date)
        query = query.group_by(TStaffServing.served_date, TStaffServing.shift_id,
                               TStaffServing.meal_id, TStaffServing.serving_id)\
            .order_by(TStaffServing.served_date)

        if list_staff_id is None or len(list_staff_id) == 0:
            ret = query.all()
        else:
            # because of pyodbc LIMITATION, prevent query over 2100 parameter
            ret = exec_query_get_list(query, TStaffServing.staff_id, list_staff_id)
        return ret

    @staticmethod
    def get_dept_report_list(db, report_filter):
        """
        get list of staff serving filtered by factory id, staff id, shift_id, meal_id, serving_id, start_date, end_date, month
        """
        list_staff_id = None
        if report_filter.department_id is not None:
            list_staff_id = StaffSql.get_staff_id_all(db, report_filter.department_id)
        # make query
        query = db.session.query(TStaffServing.served_date, TStaffServing.shift_id, TStaffServing.meal_id,
                                 TStaffServing.serving_id,
                                 func.count(TStaffServing.staff_id).label('total'))
        if report_filter.factory_id is not None:
            query = query.filter(TStaffServing.factory_id == report_filter.factory_id)
        if report_filter.staff_id is not None:
            query = query.filter(TStaffServing.staff_id == report_filter.staff_id)
        if report_filter.shift_id is not None:
            query = query.filter(TStaffServing.shift_id == report_filter.shift_id)
        if report_filter.meal_id is not None:
            query = query.filter(TStaffServing.meal_id == report_filter.meal_id)
        if report_filter.serving_id is not None:
            query = query.filter(TStaffServing.serving_id == report_filter.serving_id)
        if report_filter.start_date is not None and report_filter.end_date is not None:
            query = query.filter(TStaffServing.served_date >= report_filter.start_date,
                                 TStaffServing.served_date <= report_filter.end_date)
        if report_filter.month is not None:
            from smartcanteen.util.common import Util
            start_date, end_date = Util.get_month_range(report_filter.month)
            query = query.filter(TStaffServing.served_date >= start_date,
                                 TStaffServing.served_date <= end_date)
        query = query.group_by(TStaffServing.served_date, TStaffServing.shift_id,
                               TStaffServing.meal_id, TStaffServing.serving_id) \
            .order_by(TStaffServing.served_date)

        if list_staff_id is None or len(list_staff_id) == 0:
            ret = query.all()
        else:
            # because of pyodbc LIMITATION, prevent query over 2100 parameter
            ret = exec_query_get_list(query, TStaffServing.staff_id, list_staff_id)
        return ret

    @staticmethod
    def is_serving_existing(db, id):
        """
        Check if serving is existing in t_staff_serving table
        :return: true: existing, false: not existing
        """
        ret = db.session.query(TStaffServing.serving_id).filter(TStaffServing.serving_id == id).first()
        return ret is not None

    @staticmethod
    def is_shift_existing(db, id):
        """
        Check if shift is existing in t_staff_serving table
        :return: true: existing, false: not existing
        """
        ret = db.session.query(TStaffServing.shift_id).filter(TStaffServing.shift_id == id).first()
        return ret is not None

    @staticmethod
    def is_meal_existing(db, id):
        """
        Check if meal is existing in t_staff_serving table
        :return: true: existing, false: not existing
        """
        ret = db.session.query(TStaffServing.meal_id).filter(TStaffServing.meal_id == id).first()
        return ret is not None

    @staticmethod
    def is_line_existing(db, id):
        """
        Check if line is existing in t_staff_serving table
        :return: true: existing, false: not existing
        """
        ret = db.session.query(TStaffServing.line_id).filter(TStaffServing.line_id == id).first()
        return ret is not None

    @staticmethod
    def is_staff_existing(db, id):
        """
        Check if staff is existing in t_staff_serving table
        :return: true: existing, false: not existing
        """
        ret = db.session.query(TStaffServing.staff_id).filter(TStaffServing.staff_id == id).first()
        return ret is not None


class StaffRegisterSql:
    # add staff_info into staff_register
    @staticmethod
    def add(db, staff):
        """
        Add staff_info to t_staff_register table
        :return:
        """
        staff.datetime = datetime.now()
        staff.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(staff)

    @staticmethod
    def is_serving_existing(db, id):
        """
        Check if serving is existing in t_staff_register table
        :return: true: existing, false: not existing
        """
        ret = db.session.query(TStaffRegister.serving_id).filter(TStaffRegister.serving_id == id).first()
        return ret is not None

    @staticmethod
    def is_shift_existing(db, id):
        """
        Check if shift is existing in t_staff_register table
        :return: true: existing, false: not existing
        """
        ret = db.session.query(TStaffRegister.shift_id).filter(TStaffRegister.shift_id == id).first()
        return ret is not None

    @staticmethod
    def get_staff_serving_register_list(db,
                                        registered_date_list=None,
                                        staff_id_list=None,
                                        line_list=None,
                                        shift_id_list=None,
                                        meal_id_list=None,
                                        factory_id=None,
                                        registered_by=None,
                                        sort=False):
        """
        Check if staff_register is existing in m_staff_register table
        :return: staff register list ([TStaffRegister])
        """
        query = db.session.query(TStaffRegister).filter(
            TStaffRegister.factory_id == factory_id
        )
        if line_list is not None:
            query = query.filter(TStaffRegister.productline_id.in_(line_list))
        if registered_date_list is not None:
            query = query.filter(TStaffRegister.registered_date.in_(registered_date_list))
        if shift_id_list is not None:
            query = query.filter(TStaffRegister.shift_id.in_(shift_id_list))
        if meal_id_list is not None:
            query = query.filter(TStaffRegister.meal_id.in_(meal_id_list))
        if registered_by is not None:
            query = query.filter(TStaffRegister.registered_by == registered_by)
        if sort is True:
            query = query.order_by(TStaffRegister.registered_date)

        if staff_id_list is None or len(staff_id_list) == 0:
            ret = query.all()
        else:
            # because of pyodbc LIMITATION, prevent query over 2100 parameter
            ret = exec_query_get_list(query, TStaffRegister.staff_id, staff_id_list)
        return ret

    @staticmethod
    def get_staff_serving_register_registered_display(db,
                                                      registered_date_list=None,
                                                      staff_id_list=None,
                                                      line_list=None,
                                                      shift_id_list=None,
                                                      meal_id_list=None,
                                                      factory_id=None,
                                                      shift_id_switch_list=None,
                                                      meal_id_switch_list=None,
                                                      registered_by=None,
                                                      sort=False):
        """
        Check if staff_register is existing in m_staff_register table
        :return: staff register list ([TStaffRegister])
        """
        query = db.session.query(TStaffRegister).filter(
            TStaffRegister.factory_id == factory_id
        )
        if line_list is not None:
            query = query.filter(TStaffRegister.productline_id.in_(line_list))
        if registered_date_list is not None:
            query = query.filter(TStaffRegister.registered_date.in_(registered_date_list))
        if shift_id_list is not None:
            query = query.filter(or_(TStaffRegister.shift_id.in_(shift_id_list),
                                     TStaffRegister.meal_id.in_(meal_id_list)),
                                 or_(TStaffRegister.shift_id.in_(shift_id_switch_list),
                                     TStaffRegister.meal_id.in_(meal_id_switch_list),
                                     TStaffRegister.registered_by == registered_by,
                                     TStaffRegister.manual_confirmed == DBConst.MANUAL_CONFIRMED))
        if sort is True:
            query = query.order_by(TStaffRegister.registered_date)

        if staff_id_list is None or len(staff_id_list) == 0:
            ret = query.all()
        else:
            # because of pyodbc LIMITATION, prevent query over 2100 parameter
            ret = exec_query_get_list(query, TStaffRegister.staff_id, staff_id_list)
        return ret

    # get servings of one staff in one date
    @staticmethod
    def get_staff_serving_register_by_staff_id(db, staff_id=None, registered_date_list=None, shift_id_list=None,  factory_id=None):
        """
        :param db: Database object access
        :param staff_id: staff id
        :param registered_date: registered_date
        :param shift_id: shift_id
        :param factory_id: factory_id
        :return: [TStaffRegister]
        """
        query = db.session.query(TStaffRegister)\
                .filter(TStaffRegister.staff_id == staff_id,
                        TStaffRegister.registered_date.in_(registered_date_list),
                        TStaffRegister.shift_id.in_(shift_id_list),
                        TStaffRegister.factory_id == factory_id)
        ret = query.all()
        return ret

    @staticmethod
    def get_staff_register_kitchen_report(db, factory_id=None, registered_date_list=None, shift_id_list=None, meal_id_list=None, manual_confirmed=None):
        """
        Get kitchen report
        :return: kitchen report list ([TStaffRegister])
        """
        query = db.session.query(TStaffRegister.registered_date, TStaffRegister.shift_id, TStaffRegister.meal_id, TStaffRegister.serving_id,
                                 func.count(TStaffRegister.staff_id).label('total'))\
            .filter(TStaffRegister.registered_date.in_(registered_date_list),
                    TStaffRegister.factory_id == factory_id,
                    TStaffRegister.shift_id.in_(shift_id_list),
                    TStaffRegister.meal_id.in_(meal_id_list),
                    TStaffRegister.manual_confirmed == manual_confirmed
                    )
        ret = query.group_by(TStaffRegister.registered_date, TStaffRegister.shift_id, TStaffRegister.meal_id, TStaffRegister.serving_id).all()
        return ret

    @staticmethod
    def get_kitchen_serving_confirm(db, factory_id=None, registered_date_list=None, shift_id_list=None, meal_id_list=None,
                                    manual_confirmed=None):
        """
        Get kitchen report
        :return: kitchen report list ([TStaffRegister])
        """
        query = db.session.query(TStaffRegister.registered_date, TStaffRegister.shift_id, TStaffRegister.meal_id,
                                 TStaffRegister.serving_id, func.count(TStaffRegister.staff_id).label('total'))\
            .filter(TStaffRegister.registered_date.in_(registered_date_list),
                    TStaffRegister.factory_id == factory_id,
                    TStaffRegister.shift_id.in_(shift_id_list),
                    TStaffRegister.meal_id.in_(meal_id_list),
                    TStaffRegister.manual_confirmed == manual_confirmed)
        ret = query.group_by(TStaffRegister.registered_date, TStaffRegister.shift_id, TStaffRegister.meal_id,
                             TStaffRegister.serving_id)\
            .order_by(TStaffRegister.registered_date)\
            .all()
        return ret

    @staticmethod
    def is_meal_existing(db, id):
        """
        Check if meal is existing in t_staff_register table
        :return: true: existing, false: not existing
        """
        ret = db.session.query(TStaffRegister.meal_id).filter(TStaffRegister.meal_id == id).first()
        return ret is not None

    @staticmethod
    def is_staff_existing(db, id):
        """
        Check if staff is existing in t_staff_register table
        :return: true: existing, false: not existing
        """
        ret = db.session.query(TStaffServing.staff_id).filter(TStaffServing.staff_id == id).first()
        return ret is not None

    @staticmethod
    def get_staff_serving_report_list(db, report_filter, manual_confirmed, department_id_list=None):
        """
        get list of staff register filtered by factory id, staff id, shift_id, meal_id, serving_id, start_date, end_date, month
        """
        list_staff_id = None
        if department_id_list is not None:
            list_staff_id = StaffSql.get_staff_id_all_filter_by_department_list(db, department_id_list)
        # make query
        query = db.session.query(TStaffRegister.registered_date, TStaffRegister.shift_id, TStaffRegister.meal_id,
                                 TStaffRegister.serving_id,
                                 func.count(TStaffRegister.staff_id).label('total'))\
                          .filter(TStaffRegister.manual_confirmed == manual_confirmed)

        if report_filter.factory_id is not None:
            query = query.filter(TStaffRegister.factory_id == report_filter.factory_id)
        if report_filter.staff_id is not None:
            query = query.filter(TStaffRegister.staff_id == report_filter.staff_id)
        if report_filter.shift_id is not None:
            query = query.filter(TStaffRegister.shift_id == report_filter.shift_id)
        if report_filter.meal_id is not None:
            query = query.filter(TStaffRegister.meal_id == report_filter.meal_id)
        if report_filter.serving_id is not None:
            query = query.filter(TStaffRegister.serving_id == report_filter.serving_id)
        if report_filter.start_date is not None and report_filter.end_date is not None:
            query = query.filter(TStaffRegister.registered_date >= report_filter.start_date,
                                 TStaffRegister.registered_date <= report_filter.end_date)
        if report_filter.month is not None:
            from smartcanteen.util.common import Util
            start_date, end_date = Util.get_month_range(report_filter.month)
            query = query.filter(TStaffRegister.registered_date >= start_date,
                                 TStaffRegister.registered_date <= end_date)
        query = query.group_by(TStaffRegister.registered_date, TStaffRegister.shift_id,
                               TStaffRegister.meal_id, TStaffRegister.serving_id) \
            .order_by(TStaffRegister.registered_date)

        if list_staff_id is None or len(list_staff_id) == 0:
            ret = query.all()
        else:
            # because of pyodbc LIMITATION, prevent query over 2100 parameter
            ret = exec_query_get_list(query, TStaffRegister.staff_id, list_staff_id)
        return ret

    @staticmethod
    def get_dept_staff_registered_report_list(db, report_filter, manual_confirmed, department_id_list=None):
        """
        get list of staff register filtered by factory id, staff id,
        shift_id, meal_id, serving_id, start_date, end_date, month
        """
        list_staff_id = None
        if department_id_list is not None:
            list_staff_id = StaffSql.get_staff_id_all_filter_by_department_list(db, department_id_list)

        # make query
        query = db.session.query(TDepartment.id, TDepartment.name, TStaffRegister.meal_id,
                                 TStaffRegister.serving_id, func.count(TStaffRegister.id).label('total')) \
            .join(TStaffRegister, TDepartment.id == TStaffRegister.department_id)
        if manual_confirmed is not None:
            query = query.filter(TStaffRegister.manual_confirmed == manual_confirmed)

        if report_filter.factory_id is not None:
            query = query.filter(TStaffRegister.factory_id == report_filter.factory_id)
        if report_filter.staff_id is not None:
            query = query.filter(TStaffRegister.staff_id == report_filter.staff_id)
        if report_filter.shift_id is not None:
            query = query.filter(TStaffRegister.shift_id == report_filter.shift_id)
        if report_filter.meal_id is not None:
            query = query.filter(TStaffRegister.meal_id == report_filter.meal_id)
        if report_filter.serving_id is not None:
            query = query.filter(TStaffRegister.serving_id == report_filter.serving_id)
        if report_filter.start_date is not None and report_filter.end_date is not None:
            query = query.filter(TStaffRegister.registered_date >= report_filter.start_date,
                                 TStaffRegister.registered_date <= report_filter.end_date)
        if report_filter.month is not None:
            from smartcanteen.util.common import Util
            start_date, end_date = Util.get_month_range(report_filter.month)
            query = query.filter(TStaffRegister.registered_date >= start_date,
                                 TStaffRegister.registered_date <= end_date)

        query = query.group_by(TDepartment.id, TDepartment.name,
                               TStaffRegister.meal_id, TStaffRegister.serving_id)

        if list_staff_id is None or len(list_staff_id) == 0:
            ret = query.all()
        else:
            # because of pyodbc LIMITATION, prevent query over 2100 parameter
            ret = exec_query_get_list(query, TStaffRegister.staff_id, list_staff_id)
        return ret

    @staticmethod
    def is_meal_manual_confirmed(db, shift_id, meal_id, registered_date, registered_by=None):
        query = db.session.query(TStaffRegister.registered_date, TStaffRegister.shift_id, TStaffRegister.meal_id,
                                 TStaffRegister.serving_id, TStaffRegister.staff_id, TStaffRegister.staff_name, TStaffRegister.registered_by)\
            .filter(TStaffRegister.manual_confirmed == DBConst.MANUAL_CONFIRMED,
                    TStaffRegister.registered_date == registered_date,
                    TStaffRegister.shift_id == shift_id,
                    TStaffRegister.meal_id == meal_id)

        if registered_by is not None:
            query = query.filter(TStaffRegister.registered_by == registered_by)
        ret = query.all()
        if len(ret) == 0:
            return False
        return True

    @staticmethod
    def get_shift_list_current_registered_by_user(db, registered_day, registered_by=None):
        if registered_by is not None:
            query = db.session.query(TStaffRegister.shift_id, TStaffRegister.meal_id, TStaffRegister.registered_date) \
                .filter(TStaffRegister.manual_confirmed == DBConst.MANUAL_CONFIRMED,
                        TStaffRegister.registered_date >= registered_day,
                        TStaffRegister.registered_by == registered_by)
        else:
            query = db.session.query(TStaffRegister.shift_id, TStaffRegister.meal_id, TStaffRegister.registered_date) \
                .filter(TStaffRegister.manual_confirmed == DBConst.MANUAL_CONFIRMED,
                        TStaffRegister.registered_date >= registered_day)
        query = query.group_by(TStaffRegister.shift_id, TStaffRegister.meal_id, TStaffRegister.registered_date)
        ret = query.all()
        return ret


class LineShiftMealServingSql:
    @staticmethod
    def get_line_shift_meal_serving_list(db, factory_id):
        """
        Get line shift meal serving list  in m_line_shift_meal_serving table filter to factory_id
        :return: line shift meal serving  (list)
        """
        query = db.session.query(MLineShiftMealServing)
        if factory_id is not None:
            ret = query.filter(MLineShiftMealServing.factory_id == factory_id).all()
            return ret
        return []

    @staticmethod
    def get_line_shift_meal_serving(db, id):
        """
        Get line shift meal serving list  in m_line_shift_meal_serving table filter to factory_id
        :return: line shift meal serving  (list)
        """
        ret = db.session.query(MLineShiftMealServing).filter(MLineShiftMealServing.id == id).first()
        return ret

    @staticmethod
    def is_line_shift_meal_serving_existing(db, id=None, line_id=None, shift_meal_serving_id=None, group_line_id=None, factory_id=None):
        """
        Check if line and shift_meal_serving is existing in m_shift_meal table
        :return: true: existing, false: not existing
        """
        query = db.session.query(MLineShiftMealServing.id,
                                 MLineShiftMealServing.line_id,
                                 MLineShiftMealServing.shift_meal_serving_id,
                                 MLineShiftMealServing.group_line_id)
        if id is not None:
            query = query.filter(MLineShiftMealServing.id == id)
        if factory_id is not None:
            query = query.filter(MLineShiftMealServing.factory_id == factory_id)
        if line_id is not None:
            query = query.filter(MLineShiftMealServing.line_id == line_id)
        if shift_meal_serving_id is not None:
            query = query.filter(MLineShiftMealServing.shift_meal_serving_id == shift_meal_serving_id)
        if group_line_id is not None:
            query = query.filter(MLineShiftMealServing.group_line_id == group_line_id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def add(db, line_server_info):
        """
        Add  line_server_info to line_shift_meal_serving table
        :return:
        """
        line_server_info.created = datetime.now()
        line_server_info.upd_count = DbDefault.UPDATED_COUNT.value
        # line_server_info.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(line_server_info)

    @staticmethod
    def update(db, line_shift_meal_serving_id, line_server_info):
        """
        Edit line and shift_meal_serving to DB
        :return:
        """
        db_ln_sm_serving = db.session.query(MLineShiftMealServing).filter_by(id=line_shift_meal_serving_id).first()
        db_ln_sm_serving.line_id = line_server_info.line_id
        db_ln_sm_serving.shift_meal_serving_id = line_server_info.shift_meal_serving_id
        if line_server_info.group_line_id is not None:
            db_ln_sm_serving.group_line_id = line_server_info.group_line_id
        else:
            db_ln_sm_serving.group_line_id = None
        db_ln_sm_serving.modified = datetime.now()
        db_ln_sm_serving.upd_count = (db_ln_sm_serving.upd_count + 1) if db_ln_sm_serving.upd_count is not None else DbDefault.UPDATED_COUNT.value

    @staticmethod
    def delete(db, line_shift_meal_serving_id):
        """
        Delete line shift_meal serving from m_line_shift_meal_serving table
        :param db: DbAccess object (DbAccess)
        :param line_shift_meal_serving_id: id line shift meal serving info(m_line_shift_meal_serving model)
        :return:
        """
        db.session.query(MLineShiftMealServing).filter(MLineShiftMealServing.id == line_shift_meal_serving_id).delete()

    @staticmethod
    def is_shift_meal_serving_existing(db, shift_meal_serving_id):
        """
        :param db:
        :param shift_meal_serving_id:
        :return:
        """
        ret = db.session.query(MLineShiftMealServing).filter(MLineShiftMealServing.shift_meal_serving_id == shift_meal_serving_id).first()
        return ret is not None

    @staticmethod
    def get_line_id_all(db, factory_id=None):
        """
        :param db:
        :param factory_id:
        :return:
        """
        line_query = db.session.query(MLineShiftMealServing.line_id).filter(MLineShiftMealServing.factory_id == factory_id)\
                    .group_by(MLineShiftMealServing.line_id)\
                    .order_by(MLineShiftMealServing.line_id)\
                    .all()
        list_line_id = [id[0] for id in line_query]
        return list_line_id

    @staticmethod
    def get_line_serving(db, line_id):
        """
        Get line shift meal serving in m_line_shift_meal_serving table filter to factory_id
        :return: line shift meal serving  (list)
        """
        serving_query = db.session.query(distinct(MServing.id))\
                .filter(MLineShiftMealServing.shift_meal_serving_id == MShiftMealServing.id, MServing.id == MShiftMealServing.serving_id,
                MLineShiftMealServing.line_id == line_id)
        list_serving_id = [id[0] for id in serving_query]
        return list_serving_id

    @staticmethod
    def delete_shift_meal_serving_id(db, shift_meal_serving_id):
        """
        Delete line shift_meal serving from m_line_shift_meal_serving table
        :param db: DbAccess object (DbAccess)
        :param shift_meal_serving_id: id  shift meal serving info(m_line_shift_meal_serving model)
        :return:
        """
        db.session.query(MLineShiftMealServing)\
            .filter(MLineShiftMealServing.shift_meal_serving_id == shift_meal_serving_id).delete()

    @staticmethod
    def get_line_shift_meal_serving_by_group(db, group_line_id=None, factory_id=None):
        """
        Delete line shift_meal serving from m_line_shift_meal_serving table
        :param db: DbAccess object (DbAccess)
        :param group_line_id: id  shift meal serving info(m_line_shift_meal_serving model)
        :param factory_id: id  shift meal serving info(m_line_shift_meal_serving model)
        :return:
        """
        query = db.session.query(MLineShiftMealServing)
        if factory_id is not None:
            query = query.filter(MLineShiftMealServing.factory_id == factory_id)
        if group_line_id is not None:
            query = query.filter(MLineShiftMealServing.group_line_id == group_line_id)
        db_ret = query.all()
        return db_ret

    @staticmethod
    def get_line_served_list(db, id=None, line_id=None, shift_meal_serving_id=None, group_line_id=None, factory_id=None):
        """
        Check if line and shift_meal_serving is existing in m_shift_meal table
        :return: true: existing, false: not existing
        """
        query = db.session.query(MLineShiftMealServing.id,
                                 MLineShiftMealServing.line_id,
                                 MLineShiftMealServing.shift_meal_serving_id,
                                 MLineShiftMealServing.group_line_id)
        if id is not None:
            query = query.filter(MLineShiftMealServing.id == id)
        if factory_id is not None:
            query = query.filter(MLineShiftMealServing.factory_id == factory_id)
        if line_id is not None:
            query = query.filter(MLineShiftMealServing.line_id == line_id)
        if shift_meal_serving_id is not None:
            query = query.filter(MLineShiftMealServing.shift_meal_serving_id == shift_meal_serving_id)
        if group_line_id is not None:
            query = query.filter(MLineShiftMealServing.group_line_id == group_line_id)
        return query.all()


class ShiftSql:
    @staticmethod
    def get_shift_name(db, id):
        """
        :param db:
        :param id:
        :return:
        """
        query = db.session.query(MShift.name)
        if id is not None:
            query = query.filter(MShift.id == id)
        ret = query.first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def get_shift_name_dict(db, factory_id=None):
        """
        Get all shift name in m_shift table
        :return: Shift name dict {id: name}
        """
        query = db.session.query(MShift)
        if factory_id is not None:
            query = query.filter(MShift.factory_id == factory_id)
        db_ret = query.all()
        ret = {}
        if db_ret is not None:
            for item in db_ret:
                ret[item.id] = item.name
        return ret

    @staticmethod
    def get_shift_dict(db, factory_id):
        """
        Get shift list from shift table
        :param factory_id: factory id
        :return: shift dict {id: shift}
        """
        query = db.session.query(MShift).filter(MShift.factory_id == factory_id)
        ret = query.all()
        ret_dict = {}
        if ret is not None:
            for item in ret:
                ret_dict[item.id] = item
        return ret_dict

    @staticmethod
    def get_shift_list(db, factory_id=None):
        """
        :param db:
        :param factory_id:
        :return: [MShift]
        """
        query = db.session.query(MShift)
        if factory_id is not None:
            query = query.filter(MShift.factory_id == factory_id)
        ret = query.all()
        return ret

    @staticmethod
    def get_shift(db, factory_id, shift_id):
        """
        :return: MShift
        """
        query = db.session.query(MShift)
        if factory_id is not None:
            query = query.filter(MShift.factory_id == factory_id, MShift.id == shift_id)
        ret = query.first()
        return ret

    @staticmethod
    def is_shift_existing(db, id, factory_id=None):
        """
        Check if shift is existing in m_shift table
        :return: true: existing, false: not existing
        """
        query = db.session.query(MShift).filter(MShift.id == id)
        if factory_id is not None:
            query = query.filter(MShift.factory_id == factory_id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def add(db, shift):
        """
        :param db:
        :param shift:
        :return:
        """
        shift.created = datetime.now()
        shift.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(shift)

    @staticmethod
    def update(db, id, shift):
        """
        :param db:
        :param id:
        :param shift:
        :return:
        """
        db_shift = db.session.query(MShift).filter(MShift.id == id).first()
        db_shift.name = shift.name
        db_shift.start_time = shift.start_time
        db_shift.end_time = shift.end_time
        # Auto update
        db_shift.modified = datetime.now()
        db_shift.upd_count = (db_shift.upd_count + 1) if db_shift.upd_count is not None else DbDefault.UPDATED_COUNT.value

    @staticmethod
    def delete(db, id):
        """
        :param db:
        :param id:
        :return:
        """
        db.session.query(MShift.id).filter(MShift.id == id).delete()

    @staticmethod
    def get_shift_id_list(db, factory_id=None):
        """
        :param db:
        :param factory_id:
        :return: [MShift]
        """
        query = db.session.query(MShift.id)
        if factory_id is not None:
            query = query.filter(MShift.factory_id == factory_id)
        list_shift_id = [id[0] for id in query]
        return list_shift_id


class DepartmentSql:
    @staticmethod
    def is_department_existing(db, id, factory_id=None):
        """
        Check if department is existing in m_department table
        :return: true: existing, false: not existing
        """
        query = db.session.query(TDepartment).filter(TDepartment.id == id)
        if factory_id is not None:
            query = query.filter(TDepartment.factory_id == factory_id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def get_department_name(db, id):
        query = db.session.query(TDepartment.name)
        if id is not None:
            query = query.filter(TDepartment.id == id)
        ret = query.first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def get_department_list(db, factory_id=None):
        """
        Get department list
        :return: [TDepartment]
        """
        query = db.session.query(TDepartment)
        if factory_id is not None:
            query = query.filter(TDepartment.factory_id == factory_id)
        ret = query.all()
        return ret

    @staticmethod
    def get_department_name_dict(db, factory_id=None):
        """
        Get department dict
        :return: {id: name}
        """
        query = db.session.query(TDepartment.id, TDepartment.name)
        if factory_id is not None:
            query = query.filter(TDepartment.factory_id == factory_id)
        ret = query.all()
        ret_dict = {}
        if ret is not None:
            for item in ret:
                ret_dict[item[0]] = item[1]
        return ret_dict

    @staticmethod
    def get_department_dict(db, factory_id=None, primedepart_id=None):
        """
        Get department list from t_department table
        :param factory_id: factory id
        :return:department dict {id: name}
        """
        query = db.session.query(TDepartment)
        if factory_id is not None:
            query = query.filter(TDepartment.factory_id == factory_id)
        if primedepart_id is not None:
            query = query.filter(TDepartment.prime_department_id == primedepart_id)

        ret = query.all()
        ret_dict = {}
        if ret is not None:
            for item in ret:
                ret_dict[item.id] = item
        return ret_dict

    @staticmethod
    def get_department_sort_dict(db, factory_id=None, primedepart_id=None, sort_request=False):
        """
        Get department list from t_department table
        :param factory_id: factory id
        :return:department dict {id: name}
        """
        query = db.session.query(TDepartment)
        if primedepart_id is not None:
            query = query.filter(TDepartment.factory_id == factory_id)

        if primedepart_id is not None:
            query = query.filter(TDepartment.prime_department_id == primedepart_id)
        if sort_request:
            query = query.order_by(TDepartment.prime_department_id)

        ret = query.all()
        ret_dict = {}
        if ret is not None:
            for item in ret:
                ret_dict[item.id] = item
        return ret_dict


class StaffSql:
    @staticmethod
    def get_staff_list(db, factory_id=None, department_id=None, productline_id=None, vtm=None):
        """
        :param db:
        :param factory_id:
        :return:
        """
        query = db.session.query(TStaff)
        if factory_id is not None:
            query = query.filter(TStaff.factory_id == factory_id)
        if department_id is not None:
            query = query.filter(TStaff.department_id == department_id)
        if productline_id is not None:
            query = query.filter(TStaff.productline_id == productline_id)
        if vtm is not None:
            query = query.filter(TStaff.vtm == vtm)
        ret = query.all()
        return ret

    @staticmethod
    def get_checked_in_staff_list(db, factory_id, shift_date, shift_list, line_list):
        """
        get checked in staff from m_staff table
        :return: staff list [TStaff]
        """
        query = db.session.query(TStaff)\
            .filter(TStaff.factory_id == factory_id,
                    or_(TStaff.deleted.is_(None),
                        TStaff.deleted != DBConst.DELETED),
                    or_(TStaff.vtm == DBConst.NOT_VTM,
                        TStaff.last_checkedin >= shift_date)
                    )
        if shift_list is not None:
            query = query.filter(TStaff.shift_id.in_(shift_list))
        if line_list is not None:
            query = query.filter(TStaff.productline_id.in_(line_list))
        ret = query.order_by(TStaff.id).all()
        return ret

    @staticmethod
    def get_staff(db, id):
        """
        get staff from m_staff table
        :param id: staff_id
        :return: true: existing, false: not existing
        """
        query = db.session.query(TStaff).filter(TStaff.id == id)
        ret = query.first()
        return ret

    @staticmethod
    def get_staff_id_all(db, department_id=None):
        staff_query = db.session.query(TStaff.id)
        if department_id is not None:
            staff_query = staff_query.filter(TStaff.department_id == department_id).all()
            list_staff_id = [id[0] for id in staff_query]
            return list_staff_id

    @staticmethod
    def get_staff_id_all_filter_by_department_list(db, department_id_list=None):
        staff_query = db.session.query(TStaff.id)
        if department_id_list is not None:
            staff_query = staff_query.filter(TStaff.department_id.in_(department_id_list)).all()
            list_staff_id = [id[0] for id in staff_query]
            return list_staff_id

    @staticmethod
    def get_staff_id_list_by_dept(db, dept_id):
        """
        :param db:
        :param dept_id: department id to filter
        :return:
        """
        query = db.session.query(TStaff.id).filter(TStaff.department_id == dept_id)
        ret_list = query.all()
        if ret_list is not None:
            return [item[0] for item in ret_list]
        return []

    @staticmethod
    def get_staff_dict(db, factory_id=None):
        """
        get staff from m_staff table
        :return: staff info dict {id: TStaff}
        """
        query = db.session.query(TStaff)
        if factory_id is not None:
            query = query.filter(TStaff.factory_id == factory_id)
        ret = query.all()
        ret_dict = {}
        for item in ret:
            ret_dict[item.id] = item
        return ret_dict

    @staticmethod
    def is_staff_existing(db, id, factory_id=None):
        """
        :param db:
        :param staff_id:
        :param factory_id:
        :return:
        """
        query = db.session.query(TStaff.id).filter(TStaff.id == id)
        if factory_id is not None:
            query = query.filter(TStaff.factory_id == factory_id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def get_staff_id_by_all_dept(db, factory_id):
        query = db.session.query(TStaff.id, TDepartment)\
            .join(TDepartment, TStaff.department_id == TDepartment.id)\
            .filter(TStaff.factory_id == factory_id)
        ret = query.all()
        ret_dict = {}
        if ret is not None:
            for item in ret:
                ret_dict[item[0]] = item[1]
        return ret_dict

    @staticmethod
    def add(db, staff):
        """
        :param db:
        :param staff:
        :return:
        """
        staff.created = datetime.now()
        db.session.add(staff)

    @staticmethod
    def update(db, staff_id, staff):
        """
        :param db:
        :param staff:
        :return:
        """
        db_staff = db.session.query(TStaff).filter_by(id=staff_id).first()
        db_staff.name = staff.name
        db_staff.department_id = staff.department_id
        db_staff.productline_id = staff.productline_id
        db_staff.deleted = staff.deleted
        db_staff.shift_id = staff.shift_id

    @staticmethod
    def delete(db, id):
        """
        :param db:
        :param id:
        :return:
        """
        staff = db.session.query(TStaff).filter(TStaff.id == id).first()
        staff.deleted = DBConst.NOT_USE


class StaffFingerSql:
    @staticmethod
    def is_line_existing(db, id):
        """
        Check if line_id is existing in m_finger table
        :param id: line_id
        :return: true: existing, false: not existing
        """
        query = db.session.query(TStaffFinger).filter(TStaffFinger.line_id == id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def is_staff_existing(db, id):
        """
        Check if staff is existing in t_staff_finger table
        :return: true: existing, false: not existing
        """
        ret = db.session.query(TStaffFinger.staff_id).filter(TStaffFinger.staff_id == id).first()
        return ret is not None


class ProductLineSql:
    @staticmethod
    def get_list(db, factory_id=None, department_id=None):
        """
        Get line list from t_productline table
        :param factory_id: factory id
        :return: line list [TProductLine]
        """
        query = db.session.query(TProductLine)
        if factory_id is not None:
            query = query.filter(TProductLine.factory_id == factory_id)
        if department_id is not None:
            query = query.filter(TProductLine.department_id == department_id)
        ret = query.all()
        return ret

    @staticmethod
    def get_productline_dict(db, factory_id, department_id=None):
        """
        Get product line list from t_productline table
        :param factory_id: factory id
        :param department_id: department id
        :return: product line dict {id: name}
        """
        query = db.session.query(TProductLine).filter(TProductLine.factory_id == factory_id)
        if department_id is not None:
            query = query.filter(TProductLine.department_id == department_id)
        ret = query.all()
        ret_dict = {}
        if ret is not None:
            for item in ret:
                ret_dict[item.id] = item
        return ret_dict

    @staticmethod
    def is_existing(db, id, factory_id=None, department_id=None):
        """
        Get line list from t_productline table
        :param factory_id: factory id
        :param department_id: department id
        :return: line list [TProductLine]
        """
        query = db.session.query(TProductLine).filter(TProductLine.id == id)
        if factory_id is not None:
            query = query.filter(TProductLine.factory_id == factory_id)
        if department_id is not None:
            query = query.filter(TProductLine.department_id == department_id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def get_all_productline_list(db, factory_id=None, department_id=None):
        query = db.session.query(TProductLine.productline_id)
        if factory_id is not None:
            query = query.filter(TProductLine.factory_id == factory_id)
        if department_id is not None:
            query = query.filter(TProductLine.department_id == department_id)
        db_ret = query.all()
        if db_ret is not None and len(db_ret) > 0:
            return [item[0] for item in db_ret]

    @staticmethod
    def get_all_productline_in_department_list(db, factory_id=None, department_list=None):
        query = db.session.query(TProductLine.productline_id)
        if factory_id is not None:
            query = query.filter(TProductLine.factory_id == factory_id)
        if department_list is not None:
            query = query.filter(MKitchenStatusRegistration.shift_id.in_(department_list))
        db_ret = query.all()
        ret_dict = {}
        if db_ret is not None:
            for item in db_ret:
                ret_dict[item.id] = item
        return ret_dict


class KitchenSql:
    @staticmethod
    def get_list(db, factory_id):
        """
        Get kitchen report list from r_kitchen table
        :param factory_id: factory id
        :return: line list [RKitchen]
        """
        query = db.session.query(RKitchen).filter(RKitchen.factory_id == factory_id)
        ret = query.all()
        return ret


class UserDepartmentSql:
    @staticmethod
    def get_list(db, factory_id, user_id, department_id):
        """
        Get user department from m_user_department table
        :return: line list [MUserDepartment]
        """
        query = db.session.query(MUserDepartment).filter(MUserDepartment.factory_id == factory_id)

        if user_id is not None:
            query = query.filter(TStaff.user_id == user_id)
        if department_id is not None:
            query = query.filter(TStaff.department_id == department_id)

        ret = query.all()
        return ret


class UserProductLineSql:
    @staticmethod
    def get_list(db, factory_id, user_id, productline_id):
        """
        Get user productline from m_user_productline table
        :return: line list [MUserProductLine]
        """
        query = db.session.query(MUserProductLine).filter(MUserProductLine.factory_id == factory_id)

        if user_id is not None:
            query = query.filter(MUserProductLine.user_id == user_id)
        if productline_id is not None:
            query = query.filter(MUserProductLine.productline_id == productline_id)

        ret = query.all()
        return ret

    @staticmethod
    def get_productline_id_list(db, factory_id, user_id):
        """
        Get productline id from m_user_productline table
        :return: line list [MUserProductLine]
        """
        query = db.session.query(MUserProductLine.productline_id).filter(MUserProductLine.factory_id == factory_id)

        if user_id is not None:
            query = query.filter(MUserProductLine.user_id == user_id)

        db_ret = query.all()
        if db_ret is not None and len(db_ret) > 0:
            return [item[0] for item in db_ret]

    @staticmethod
    def get_user_productline(db, id):
        """
        Get user productline from m_user_productline table
        :return: line list [MUserProductLine]
        """
        query = db.session.query(MUserProductLine).filter(MUserProductLine.id == id)
        ret = query.first()
        return ret

    @staticmethod
    def get_user_productline_dict(db, factory_id=None, user_id=None):
        query = db.session.query(MUserProductLine)
        if factory_id is not None:
            query = query.filter(MUserProductLine.factory_id == factory_id)
        if user_id is not None:
            query = query.filter(MUserProductLine.user_id == user_id)
        ret = query.all()
        ret_dict = {}
        if ret is not None:
            for item in ret:
                ret_dict[item.id] = item
        return ret_dict

    @staticmethod
    def get_first_user_productline(db, user_id, line_id):
        """
        Get user productline from m_user_productline table
        :return: MUserProductLine
        """
        query = db.session.query(MUserProductLine)\
            .filter(MUserProductLine.productline_id == line_id,
                    MUserProductLine.user_id == user_id)
        ret = query.first()
        return ret

    @staticmethod
    def get_all_productline(db, user_id):
        """
        Get user productline from m_user_productline table
        :return: MUserProductLine
        """
        query = db.session.query(MUserProductLine) \
            .filter(MUserProductLine.user_id == user_id)
        ret = query.all()
        return ret

    @staticmethod
    def is_existing(db, user_id, productline_id=None, shift_id=None):
        """
        Check if productline is existing in m_user_productline table
        :return: true: existing, false: not existing
        """
        query = db.session.query(MUserProductLine).filter(MUserProductLine.user_id == user_id)
        if productline_id is not None:
            query = query.filter(MUserProductLine.productline_id == productline_id)
        if shift_id is not None:
            query = query.filter(MUserProductLine.shift_id == shift_id)

        ret = query.first()
        return ret is not None



    @staticmethod
    def is_existing_id(db, user_id, factory_id):
        """
        Check if productline is existing in m_user_productline table
        :return: true: existing, false: not existing
        """
        query = db.session.query(MUserProductLine).filter(MUserProductLine.user_id == user_id,
                                                          MUserProductLine.factory_id == factory_id)
        ret = query.first()
        return ret is not None

    @staticmethod
    def add(db, data):
        """
        Add to m_user_productline
        """
        data.created = datetime.now()
        data.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(data)

    @staticmethod
    def update(db, id, user_productline):
        """
        Edit user to m_user_productline table
        :param db: DbAccess object (DbAccess)
        :param id: user_productline id (int)
        :param user_productline: user user_productline (MUserProductLine)
        :return:
        """
        db_data = db.session.query(MUserProductLine).filter_by(id=id).first()
        db_data.user_id = user_productline.user_id
        db_data.productline_id = user_productline.productline_id
        db_data.shift_id = user_productline.shift_id
        # auto update
        db_data.modified = datetime.now()
        db_data.upd_count = (db_data.upd_count + 1) if db_data.upd_count is not None else DbDefault.UPDATED_COUNT.value

    @staticmethod
    def delete(db, user_id):
        """
        delete on row from m_user_productline
        :param db: DbAccess object (DbAccess)
        :param user_id: user product line id(id)
        :return:
        """
        db.session.query(MUserProductLine).filter(MUserProductLine.user_id == user_id).delete()


class KitchenStatusRegistrationSql:
    @staticmethod
    def get_list(db, factory_id=None, shift_id_list=None, close_date_list=None, closed_status = None):
        """
        Get kitchen status registration list from m_kitchen_status_registration table
        :return: list [MKitchenStatusRegistration]
        """
        query = db.session.query(MKitchenStatusRegistration)
        if factory_id is not None:
            query = query.filter(MKitchenStatusRegistration.factory_id == factory_id)
        if shift_id_list is not None:
            query = query.filter(MKitchenStatusRegistration.shift_id.in_(shift_id_list))
        if close_date_list is not None:
            query = query.filter(MKitchenStatusRegistration.closed_date.in_(close_date_list))
        if closed_status is not None:
            query = query.filter(MKitchenStatusRegistration.closed_status == closed_status)
        ret = query.all()
        return ret

    @staticmethod
    def get_list_kitchen_serving(db, factory_id=None, shift_id_list=None, close_date_list=None):
        """
        :param db:
        :param factory_id:
        :param shift_id_list:
        :param close_date:
        :return:
        """
        query = db.session.query(MKitchenStatusRegistration.id, MKitchenStatusRegistration.shift_id,
                                 MKitchenStatusRegistration.meal_id,
                                 MKitchenStatusRegistration.closed_status,
                                 MKitchenStatusRegistration.closed_date,
                                 MKitchenHistory.serving_id,
                                 MKitchenHistory.count_register,
                                 MKitchenHistory.count_accept)\
            .join(MKitchenHistory, MKitchenHistory.kitchen_confirm_id == MKitchenStatusRegistration.id)
        if factory_id is not None:
            query = query.filter(MKitchenStatusRegistration.factory_id == factory_id)
        if shift_id_list is not None:
            query = query.filter(MKitchenStatusRegistration.shift_id.in_(shift_id_list))
        if close_date_list is not None:
            query = query.filter(MKitchenStatusRegistration.closed_date.in_(close_date_list))
        ret = query.all()
        return ret

    @staticmethod
    def get_kitchen_serving_report_list(db, report_filter):
        """
        :param db:
        :param report_filter:
        :return:
        """
        query = db.session.query(MKitchenStatusRegistration.closed_date,
                                 MKitchenStatusRegistration.shift_id,
                                 MKitchenStatusRegistration.meal_id,
                                 MKitchenHistory.serving_id,
                                 MKitchenHistory.count_register,
                                 MKitchenHistory.count_accept) \
            .join(MKitchenHistory, MKitchenHistory.kitchen_confirm_id == MKitchenStatusRegistration.id)

        if report_filter.factory_id is not None:
            query = query.filter(MKitchenStatusRegistration.factory_id == report_filter.factory_id)
        if report_filter.shift_id is not None:
            query = query.filter(MKitchenStatusRegistration.shift_id == report_filter.shift_id)
        if report_filter.meal_id is not None:
            query = query.filter(MKitchenStatusRegistration.meal_id == report_filter.meal_id)
        if report_filter.serving_id is not None:
            query = query.filter(MKitchenHistory.serving_id == report_filter.serving_id)
        if report_filter.start_date is not None and report_filter.end_date is not None:
            query = query.filter(MKitchenStatusRegistration.closed_date >= report_filter.start_date,
                                 MKitchenStatusRegistration.closed_date <= report_filter.end_date)
        if report_filter.month is not None:
            from smartcanteen.util.common import Util
            start_date, end_date = Util.get_month_range(report_filter.month)
            query = query.filter(MKitchenStatusRegistration.closed_date >= start_date,
                                 MKitchenStatusRegistration.closed_date <= end_date)
        ret = query.all()
        return ret

    @staticmethod
    def is_meal_existing(db, id):
        """
        Check if meal is existing in m_shift_meal table
        :param id: meal_id
        :return: true: existing, false: not existing
        """
        ret = db.session.query(MKitchenStatusRegistration.meal_id).filter(MKitchenStatusRegistration.meal_id == id).first()
        return ret is not None

    @staticmethod
    def get_kitchen(db, id=None, shift_id=None, meal_id=None, date=None):
        query = db.session.query(MKitchenStatusRegistration)
        if id is not None:
            query = query.filter(MKitchenStatusRegistration.id == id)
        if shift_id is not None:
            query = query.filter(MKitchenStatusRegistration.shift_id == shift_id)
        if meal_id is not None:
            query = query.filter(MKitchenStatusRegistration.meal_id == meal_id)
        if date is not None:
            query = query.filter(MKitchenStatusRegistration.closed_date == date)
        ret = query.first()
        return ret

    @staticmethod
    def get_kitchen_confirmed_list(db, id=None, shift_id_list=None, meal_id_list=None, date_list=None):
        query = db.session.query(MKitchenStatusRegistration)
        if id is not None:
            query = query.filter(MKitchenStatusRegistration.id == id)
        if shift_id_list is not None:
            query = query.filter(MKitchenStatusRegistration.shift_id.in_(shift_id_list))
        if meal_id_list is not None:
            query = query.filter(MKitchenStatusRegistration.meal_id.in_(meal_id_list))
        if date_list is not None:
            query = query.filter(MKitchenStatusRegistration.closed_date.in_(date_list))
        ret = query.all()
        return ret

    @staticmethod
    def get_id(db, id=None, shift_id=None, meal_id=None, date=None):
        query = db.session.query(MKitchenStatusRegistration.id)
        if id is not None:
            query = query.filter(MKitchenStatusRegistration.id == id)
        if shift_id is not None:
            query = query.filter(MKitchenStatusRegistration.shift_id == shift_id)
        if meal_id is not None:
            query = query.filter(MKitchenStatusRegistration.meal_id == meal_id)
        if date is not None:
            query = query.filter(MKitchenStatusRegistration.closed_date == date)
        ret = query.first()
        if ret is not None:
            return ret[0]

    @staticmethod
    def add(db, data):
        """
        Add to m_user_productline
        """
        data.created = datetime.now()
        data.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(data)

    @staticmethod
    def is_kitchen_existing(db, id=None, factory_id=None, shift_id=None, meal_id=None, closed_date=None):
        query = db.session.query(MKitchenStatusRegistration.id)
        if id is not None:
            query = query.filter(MKitchenStatusRegistration.id == id)
        if factory_id is not None:
            query = query.filter(MKitchenStatusRegistration.factory_id == factory_id)
        if shift_id is not None:
            query = query.filter(MKitchenStatusRegistration.shift_id == shift_id)
        if meal_id is not None:
            query = query.filter(MKitchenStatusRegistration.meal_id == meal_id)
        if closed_date is not None:
            query = query.filter(MKitchenStatusRegistration.closed_date == closed_date)
        ret = query.first()
        return ret is not None


class KitchenHistorySql:
    @staticmethod
    def get_list(db, kitchen_confirm_id=None):
        """
        Get kitchen status registration list from m_kitchen_status_registration table
        :return: list [MKitchenStatusRegistration]
        """
        query = db.session.query(MKitchenHistory)
        if kitchen_confirm_id is not None:
            query = query.filter(MKitchenHistory.kitchen_confirm_id == kitchen_confirm_id)
        ret = query.all()
        return ret

    @staticmethod
    def add(db, data):
        """
        Add to m_user_productline
        """
        data.created = datetime.now()
        data.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(data)

    @staticmethod
    def is_serving_existing(db, id):
        """
        :param db:
        :param id: int
        :return: true if existing, false if not existing
        """
        ret = db.session.query(MKitchenHistory.serving_id).filter(MKitchenHistory.serving_id == id).first()
        return ret is not None


class CalendarSql:
    @staticmethod
    def get_calendar_list(db, factory_id=None, start_date=None, end_date=None):
        """
        Get list of all calendar in m_calendar table
        :param db: Database access object
        :param factory_id:
        :param start_date:
        :param: end_date
        :return: [m_calendar]
        """
        query = db.session.query(MCalendar)
        if factory_id is not None:
            query = query.filter(MCalendar.factory_id == factory_id)
        if start_date is not None:
            query = query.filter(MCalendar.start_date >= start_date)
        if end_date is not None:
            query = query.filter(MCalendar.end_date <= end_date)
        ret = query.all()
        return ret

    @staticmethod
    def get_calendar(db, id=None, factory_id=None, start_date=None, end_date=None):
        query = db.session.query(MCalendar)
        if id is not None:
            query = query.filter(MCalendar.id == id)
        if factory_id is not None:
            query = query.filter(MCalendar.factory_id == factory_id)
        if start_date is not None:
            query = query.filter(MCalendar.start_date == start_date)
        if end_date is not None:
            query = query.filter(MCalendar.end_date == end_date)
        ret = query.first()
        return ret

    @staticmethod
    def get_calendar_list_in_period(db, factory_id=None, start_date=None, end_date=None):
        query = db.session.query(MCalendar)
        if factory_id is not None:
            query = query.filter(MCalendar.factory_id == factory_id)
        if start_date is not None and end_date is not None:
            query = query.filter(or_(and_(MCalendar.start_date <= start_date, MCalendar.end_date >= start_date),
                                 and_(MCalendar.start_date <= end_date, MCalendar.end_date >= end_date),
                                 and_(MCalendar.start_date >= start_date, MCalendar.end_date <= end_date)))
        ret = query.all()
        return ret

    @staticmethod
    def get_calendar_in_period(db, factory_id=None, start_date=None, end_date=None):
        query = db.session.query(MCalendar)
        if factory_id is not None:
            query = query.filter(MCalendar.factory_id == factory_id)
        if start_date is not None and end_date is not None:
            query = query.filter(or_(and_(MCalendar.start_date <= start_date, MCalendar.end_date >= start_date),
                                 and_(MCalendar.start_date <= end_date, MCalendar.end_date >= end_date),
                                 and_(MCalendar.start_date >= start_date, MCalendar.end_date <= end_date)))
        ret = query.first()
        return ret


    @staticmethod
    def is_calendar_existing(db, id=None, factory_id=None, start_date=None, end_date=None):
        """
        Check if calendar is existing in m_calendar table
        :param id: calendar_id
        :param factory_id: factory_id
        :return: true: existing, false: not existing
        """
        query = db.session.query(MCalendar.id)
        if id is not None:
            query = query.filter(MCalendar.id == id)
        if factory_id is not None:
            query = query.filter(MCalendar.factory_id == factory_id)
        if start_date is not None:
            query = query.filter(MCalendar.start_date == start_date)
        if end_date is not None:
            query = query.filter(MCalendar.end_date == end_date)
        ret = query.first()
        return ret is not None

    @staticmethod
    def add(db, calendar):
        """
        Add to m_calendar
        """
        calendar.created = datetime.now()
        calendar.upd_count = DbDefault.UPDATED_COUNT.value
        db.session.add(calendar)

    @staticmethod
    def update(db, id, calendar):
        """
        Update to calendar
        :param db:
        :param id:
        :param calendar:
        :return:
        """
        db_calendar = db.session.query(MCalendar).filter_by(id=id).first()
        db_calendar.title = calendar.title
        db_calendar.start_date = calendar.start_date
        db_calendar.end_date = calendar.end_date
        db_calendar.date_type = calendar.date_type
        # auto update
        db_calendar.modified = datetime.now()
        db_calendar.upd_count = (db_calendar.upd_count + 1) if db_calendar.upd_count is not None else DbDefault.UPDATED_COUNT.value

    @staticmethod
    def delete(db, calendar_id):
        """
        delete one calendar
        :param db: DbAccess object (DbAccess)
        :param calendar_id: id calendar info(m_calendar model)
        :return:
        """
        db.session.query(MCalendar).filter(MCalendar.id == calendar_id).delete()


class MenuSql:
    @staticmethod
    def get_list(db):
        """
        Get list of all menu
        :param db: Database access object
        :return: [SMenu]
        """
        # Select menu
        ret_list = db.session.query(SMenu).all()
        return ret_list


class PrivilegeMenuSql:
    @staticmethod
    def get_list(db, privilege_id):
        """
        Get list of all menu access privilege
        :param db: Database access object
        :param privilege_id: Privilege id
        :return: [SPrivilegeMenu, SMenu.name]
        """
        # Select privilege
        ret = db.session.query(SPrivilegeMenu) \
            .filter(SPrivilegeMenu.privilege_id == privilege_id).all()
        return ret


class PrimeDepartmentSql:

    @staticmethod
    def get_primedepartment_list(db, factory_id=None):
        """
        Get department list
        :return: [TDepartment]
        """
        query = db.session.query(TPrimeDepartment)
        if factory_id is not None:
            query = query.filter(TPrimeDepartment.factory_id == factory_id)
        ret = query.all()
        return ret

    @staticmethod
    def get_primedepartment_name_dict(db, factory_id=None):
        """
        Get department dict
        :return: {id: name}
        """
        query = db.session.query(TPrimeDepartment.id, TPrimeDepartment.name)
        if factory_id is not None:
            query = query.filter(TPrimeDepartment.factory_id == factory_id)
        ret = query.all()
        ret_dict = {}
        if ret is not None:
            for item in ret:
                ret_dict[item[0]] = item[1]
        return ret_dict

    @staticmethod
    def get_primedepartment_dict(db, factory_id=None, primedepart_id=None, un_flag_all=False):
        """
        Get prime department list from t_department table
        :param factory_id: factory id
        :return:prime department dict {id: name}
        """
        query = db.session.query(TPrimeDepartment)

        if factory_id is not None:
            query = query.filter(TPrimeDepartment.factory_id == factory_id)
        if primedepart_id is not None:
            query = query.filter(TPrimeDepartment.prime_department_id == primedepart_id)
        if un_flag_all:
            query = query.filter(or_(TPrimeDepartment.flag_all.is_(None),
                                     TPrimeDepartment.flag_all != DBConst.FLAG_ALL))

        ret = query.all()
        ret_dict = {}
        if ret is not None:
            for item in ret:
                ret_dict[item.id] = item
        return ret_dict
