"""Common definition"""
from enum import Enum

# Config file
CFG_FILENAME = "config.ini"

# Invalid user id
VAL_INVALID_ID = -1


class DbDefault(Enum):
    """DB default value"""
    UPDATED_COUNT = 1


class UserInfo:
    def __init__(self, factory_id, user_id):
        self.factory_id = factory_id
        self.user_id = user_id


class CommonLibError(Exception):
    """CommonLib error"""

    def __init__(self, msg, original_exception=None):
        """
        :param msg: message
        :param original_exception: original exception
        """
        # Message format = [Error class name] [message]: [original exception]
        new_msg = "{0}-{1}".format(str(type(self).__name__), msg)
        if original_exception is not None:
            new_msg += ": "
            new_msg += str(original_exception)

        super(CommonLibError, self).__init__(new_msg)


class NotFoundError(CommonLibError):
    """Not existing error"""


class ConfigError(CommonLibError):
    """Conflict error"""


class DbAccessError(CommonLibError):
    """Database error"""


class AuthenticateError(CommonLibError):
    """Authentication error"""


class AuthorizationError(CommonLibError):
    """Authentication error"""


class Function(Enum):
    """Web function definition"""

    def __str__(self):
        return self.name

    def id(self):
        """
        :rtype: int
        :return: Function ID
        """
        return self.value

    # unknown
    unknown = 0

    # auth function
    login_get = 1
    login_post = 2
    logout_post = 12

    # privilege function
    privilege_get = 101

    # factory function
    factory_get = 201

    # department function
    department_get = 2101


    user_get = 1001
    user_post = 1002
    user_put = 1003
    user_delete = 1004
    user_password_put = 1005

    role_get = 1011
    role_post = 1012
    role_put = 1013
    role_delete = 1014

    user_role_get = 1021
    user_role_post = 1022
    user_role_put = 1023
    user_role_delete = 1024

    role_path_get = 1031
    role_path_post = 1032
    role_path_put = 1033
    role_path_delete = 1034

    # line function
    line_get = 2001
    line_post = 2002
    line_put = 2003
    line_delete = 2004

    scanner_get = 2011
    scanner_post = 2012
    scanner_put = 2013
    scanner_delete = 2014

    line_scanner_get = 2021
    line_scanner_post = 2022
    line_scanner_put = 2023
    line_scanner_delete = 2024

    # meal function
    meal_get = 3001
    meal_post = 3002
    meal_put = 3003
    meal_delete = 3004

    shift_meal_get = 3011
    shift_meal_post = 3012
    shift_meal_put = 3013
    shift_meal_delete = 3014

    shift_meal_serving_get = 3021
    shift_meal_serving_post = 3022
    shift_meal_serving_put = 3023
    shift_meal_serving_delete = 3024

    line_shift_meal_serving_get = 2031
    line_shift_meal_serving_post = 2032
    line_shift_meal_serving_put = 2033
    line_shift_meal_serving_delete = 2034

    serving_get = 2041
    serving_post = 2042
    serving_put = 2043
    serving_delete = 2044

    shift_get = 2051
    shift_post = 2052
    shift_put = 2053
    shift_delete = 2054

    user_department_get = 2061
    user_department_post = 2062
    user_department_put = 2063
    user_department_delete = 2064

    user_productline_get = 2071
    user_productline_post = 2072
    user_productline_put = 2073
    user_productline_delete = 2074

    canteen_display_get = 3031
    kitchen_display_get = 3032

    staff_serving_register_get = 3041
    staff_serving_register_post = 3042
    staff_serving_register_delete = 3044

    staff_serving_raw_report_post = 3051
    staff_serving_report_post = 3052
    kitchen_serving_report_post = 3053
    
    staff_serving_post = 3062

    product_line_get = 2081

    kitchen_confirm_get = 2091
    kitchen_confirm_put = 2092
    cancel_kitchen_confirm_put = 2093

    staff_get = 3071
    staff_post = 3072
    staff_put = 3073
    staff_delete = 3074

    import_staff_get = 3081
    import_staff_post = 3082

    download_get = 3091
    calendar_get = 4001
    calendar_post = 4002
    calendar_put = 4003
    calendar_delete = 4004

    # primedepartment function
    primedepartment_get = 2101

    # report department
    department_serving_report_post = 5001
    export_department_serving_report = 5002

    group_line_shift_meal_serving_get = 5100
    group_line_shift_meal_serving_post = 5101
    group_line_shift_meal_serving_put = 5102
    group_line_shift_meal_serving_delete = 5103

