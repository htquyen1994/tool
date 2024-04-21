# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Index, Integer, NCHAR, String, TEXT, Time
from sqlalchemy.dialects.mssql import DATETIME2, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MLine(Base):
    __tablename__ = 'm_line'

    id = Column(Integer, primary_key=True, autoincrement=False)
    factory_id = Column(Integer, nullable=False)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))


class MLineScanner(Base):
    __tablename__ = 'm_line_scanner'

    id = Column(Integer, primary_key=True)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    line_id = Column(Integer, nullable=False)
    scanner_id = Column(Integer, nullable=False)
    factory_id = Column(Integer, nullable=False)


class MLineShiftMealServing(Base):
    __tablename__ = 'm_line_shift_meal_serving'

    id = Column(Integer, primary_key=True)
    line_id = Column(Integer)
    shift_meal_serving_id = Column(Integer)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    factory_id = Column(Integer)
    upd_count = Column(Integer)
    group_line_id = Column(Integer)


class MGroupLineShiftMealServing(Base):
    __tablename__ = 'm_group_line_shift_meal_serving'

    id = Column(Integer, primary_key=True, autoincrement=False)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    factory_id = Column(Integer)
    upd_count = Column(Integer)
    start_serving = Column(Time)
    end_serving = Column(Time)


class MMeal(Base):
    __tablename__ = 'm_meal'

    id = Column(Integer, primary_key=True, autoincrement=False)
    factory_id = Column(Integer, nullable=False)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))


class MRole(Base):
    __tablename__ = 'm_role'

    id = Column(Integer, primary_key=True, autoincrement=False)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    privilege_id = Column(Integer, nullable=False)
    factory_id = Column(Integer)


class MScanner(Base):
    __tablename__ = 'm_scanner'

    id = Column(Integer, primary_key=True, autoincrement=False)
    factory_id = Column(Integer, nullable=False)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    ip_address = Column(String(15, 'SQL_Latin1_General_CP1_CI_AS'))


class MServing(Base):
    __tablename__ = 'm_serving'

    id = Column(Integer, primary_key=True, autoincrement=False)
    factory_id = Column(Integer, nullable=False)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    name_en = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    out_of_service = Column(Integer)


class MShift(Base):
    __tablename__ = 'm_shift'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    created = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    factory_id = Column(Integer)
    modified = Column(DATETIME2)
    start_time = Column(Time)
    end_time = Column(Time)
    group = Column(Integer)


class MShiftMeal(Base):
    __tablename__ = 'm_shift_meal'

    id = Column(Integer, primary_key=True)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    shift_id = Column(Integer, nullable=False)
    meal_id = Column(Integer, nullable=False)
    name = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    factory_id = Column(Integer, nullable=False)
    start_register = Column(Time)
    end_register = Column(Time)
    start_serving = Column(Time)
    end_serving = Column(Time)
    serving_day_after_register = Column(Integer)
    overtime = Column(Integer)
    register_until_today_plus = Column(Integer)
    default_serving_id = Column(Integer)


class MShiftMealServing(Base):
    __tablename__ = 'm_shift_meal_serving'

    id = Column(Integer, primary_key=True)
    shift_meal_id = Column(Integer, nullable=False)
    serving_id = Column(Integer, nullable=False)
    factory_id = Column(Integer, nullable=False)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))


class MUser(Base):
    __tablename__ = 'm_user'

    id = Column(Integer, primary_key=True, autoincrement=False)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    password = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    role_id = Column(Integer, nullable=False)


class MUserDepartment(Base):
    __tablename__ = 'm_user_department'

    id = Column(Integer, primary_key=True)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    factory_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    department_id = Column(Integer, nullable=False)


class MUserProductLine(Base):
    __tablename__ = 'm_user_productline'

    id = Column(Integer, primary_key=True)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    factory_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    productline_id = Column(Integer, nullable=False)
    shift_id = Column(Integer)


class SFactory(Base):
    __tablename__ = 's_factory'

    id = Column(Integer, primary_key=True, autoincrement=False)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))


class SFunction(Base):
    __tablename__ = 's_function'

    id = Column(Integer, primary_key=True, autoincrement=False)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    function = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))


class SPrivilege(Base):
    __tablename__ = 's_privilege'

    id = Column(Integer, primary_key=True, autoincrement=False)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    init_privilege = Column(Integer)


class SPrivilegeFunction(Base):
    __tablename__ = 's_privilege_function'

    id = Column(Integer, primary_key=True)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    privilege_id = Column(Integer, nullable=False)
    function_id = Column(Integer, nullable=False)


class TLineServing(Base):
    __tablename__ = 't_line_serving'

    id = Column(Integer, primary_key=True)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    line_id = Column(Integer, nullable=False)
    serving_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    shift_id = Column(Integer, nullable=False)
    factory_id = Column(Integer, nullable=False)


class TSession(Base):
    __tablename__ = 't_session'

    id = Column(Integer, primary_key=True)
    factory_id = Column(Integer)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    key = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    user_id = Column(Integer, nullable=False)
    expired = Column(DATETIME2, nullable=False)


class TStaffFinger(Base):
    __tablename__ = 't_staff_finger'

    id = Column(Integer, primary_key=True)
    staff_id = Column(Integer, nullable=False)
    line_id = Column(Integer, nullable=False)
    verify_type = Column(Integer, nullable=False)
    verify_time = Column(Time, nullable=False)
    date = Column(Date, nullable=False)
    datetime = Column(DATETIME2, nullable=False)
    result = Column(Integer)
    note = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))


class TStaffRegister(Base):
    __tablename__ = 't_staff_register'

    id = Column(Integer, primary_key=True)
    staff_id = Column(Integer)
    datetime = Column(DATETIME2)
    registered_date = Column(Date, nullable=False)
    serving_id = Column(Integer, nullable=False)
    factory_id = Column(Integer, nullable=False)
    shift_id = Column(Integer)
    meal_id = Column(Integer)
    department_id = Column(Integer)
    productline_id = Column(Integer)
    prime_department_id = Column(Integer)
    staff_name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    registered_by = Column(Integer)
    hr_shift_id = Column(Integer)
    manual_confirmed = Column(Integer)


class TStaffServing(Base):
    __tablename__ = 't_staff_serving'
    __table_args__ = (
        Index('Staff-Shift-Date-Factory', 'staff_id', 'shift_id', 'served_date', 'factory_id'),
        Index('Shift-Line-Date-Factory', 'shift_id', 'line_id', 'served_date', 'factory_id')
    )

    id = Column(Integer, primary_key=True)
    staff_id = Column(Integer)
    shift_id = Column(Integer, nullable=False)
    meal_id = Column(Integer, nullable=False)
    serving_id = Column(Integer, nullable=False)
    line_id = Column(Integer, nullable=False)
    served_date = Column(Date, nullable=False)
    factory_id = Column(Integer, nullable=False)
    datetime = Column(DATETIME2)
    staff_name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    department_id = Column(Integer)
    productline_id = Column(Integer)
    prime_department_id = Column(Integer)


class TDepartment(Base):
    __tablename__ = 't_department'

    id = Column(Integer, primary_key=True)
    created = Column(DATETIME2)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    factory_id = Column(Integer)
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    prime_department_id = Column(Integer, nullable=False)
    flag_all = Column(Integer)


class TProductLine(Base):
    __tablename__ = 't_productline'

    id = Column(Integer, primary_key=True)
    created = Column(DATETIME2)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    factory_id = Column(Integer)
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    department_id = Column(Integer, nullable=False)
    flag_all = Column(Integer)

class TStaff(Base):
    __tablename__ = 't_staff'

    id = Column(Integer, primary_key=True, autoincrement=False)
    created = Column(DATETIME2)
    last_checkedin = Column(DATETIME2)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    factory_id = Column(Integer, nullable=False)
    department_id = Column(Integer, nullable=False)
    productline_id = Column(Integer, nullable=False)
    shift_id = Column(Integer)
    deleted = Column(Integer)
    vtm = Column(Integer)
    prime_department_id = Column(Integer, nullable=False)


class THistory(Base):
    __tablename__ = 't_history'

    id = Column(Integer, primary_key=True)
    factory_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    datetime = Column(DATETIME2, nullable=False)
    user_id = Column(Integer, nullable=False)
    function_id = Column(Integer, nullable=False)
    function_name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    result = Column(Integer, nullable=False)
    note = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))


class RKitchen(Base):
    __tablename__ = 'r_kitchen'

    id = Column(Integer, primary_key=True)
    created = Column(DATETIME2)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    factory_id = Column(Integer, nullable=False)
    report_time = Column(Time)
    name = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))


class MKitchenHistory(Base):
    __tablename__ = 'm_kitchen_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    kitchen_confirm_id = Column(Integer)
    serving_id = Column(Integer)
    count_register = Column(Integer)
    count_accept = Column(Integer)
    factory_id = Column(Integer)


class MKitchenStatusRegistration(Base):
    __tablename__ = 'm_kitchen_status_registration'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    user_id = Column(Integer)
    closed_date = Column(Date)
    closed_status = Column(Integer)
    factory_id = Column(Integer)
    shift_id = Column(Integer)
    meal_id = Column(Integer)


class THrShift(Base):
    __tablename__ = 't_hr_shift'

    id = Column(Integer, primary_key=True)
    factory_id = Column(Integer, nullable=False)
    shift_id = Column(Integer, nullable=False)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    overtime = Column(Integer, nullable=False)


class MCalendar(Base):
    __tablename__ = 'm_calendar'

    id = Column(Integer, primary_key=True)
    title = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    start_date = Column(Date)
    end_date = Column(Date)
    date_type = Column(Integer)
    factory_id = Column(Integer, nullable=False)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))


class SMenu(Base):
    __tablename__ = 's_menu'

    id = Column(Integer, primary_key=True, autoincrement=False)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))


class SPrivilegeMenu(Base):
    __tablename__ = 's_privilege_menu'

    id = Column(Integer, primary_key=True)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    privilege_id = Column(Integer, nullable=False)
    menu_id = Column(Integer, nullable=False)
    default = Column(Integer, nullable=False)


class TPrimeDepartment(Base):
    __tablename__ = 't_prime_department'

    id = Column(Integer, primary_key=True)
    created = Column(DATETIME2)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    factory_id = Column(Integer)
    name = Column(String(256, 'SQL_Latin1_General_CP1_CI_AS'))
    flag_all = Column(Integer)


class MUserPrimeDepartment(Base):
    __tablename__ = 'm_user_prime_department'

    id = Column(Integer, primary_key=True)
    created = Column(DATETIME2)
    modified = Column(DATETIME2)
    upd_count = Column(Integer)
    note = Column(TEXT(2147483647, 'SQL_Latin1_General_CP1_CI_AS'))
    factory_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    prime_department_id = Column(Integer, nullable=False)
    shift_id = Column(Integer, nullable=False)