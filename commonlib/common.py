from commonlib.const import Function


class CommonUtil:
    @staticmethod
    def get_function_id(function):
        return Function[str(function)].id()
