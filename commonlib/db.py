# import urllib
#
# from sqlalchemy import create_engine
# from sqlalchemy.exc import DBAPIError, OperationalError, IntegrityError
# from sqlalchemy.engine import ResultProxy
# from sqlalchemy.orm import sessionmaker
# from config.config import MSSQL_SERVER
#
# params = 'DRIVER={0};SERVER={1};PORT={2};DATABASE={3};UID={4};PWD={5};'.format(MSSQL_SERVER.DRIVER.value,
#                                                                                MSSQL_SERVER.DB_HOST.value,
#                                                                                MSSQL_SERVER.DB_PORT.value,
#                                                                                MSSQL_SERVER.DB_NAME.value,
#                                                                                MSSQL_SERVER.DB_USER.value,
#                                                                                MSSQL_SERVER.DB_PASSWORD.value)
#
# params = urllib.parse.quote_plus(params)
#
# # engines list for each process
# g_engines = {}
#
#
# class DbAccess:
#
#     def __init__(self, engine):
#         self.connection = engine.connect()
#
#         # create a configured "Session" class
#         session_class = sessionmaker(bind=self.connection, autocommit=True)
#
#         # create a Session
#         self.session = session_class()
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_value, traceback):
#         # "print("DbAccess exit!!!")
#         self.close()
#
#     @staticmethod
#     def get_instance():
#         # global engines list for each process
#         global g_engines
#         db_name = MSSQL_SERVER.DB_NAME.value
#
#         if db_name in g_engines:
#             print(">>> Reuse SQLALCHEMY engine!!!")
#             engine = g_engines[db_name]
#         else:
#             conn_string = "mssql+pyodbc:///?odbc_connect={}".format(params)
#             # print(conn_string)
#             engine = create_engine(conn_string, echo=False, connect_args={
#                 'check_same_thread': False,
#                 'pool_size': 30,
#                 'pool_recycle': 3600,
#                 'pool_pre_ping': False,
#             })
#
#         # Save engine to global
#         g_engines[db_name] = engine
#
#         return DbAccess(engine)
#
#     def close(self):
#         if self.session:
#             self.session.close()
#             self.session = None
#         if self.connection:
#             self.connection.close()
#             self.connection = None
#
#     def begin(self):
#         if self.session:
#             self.session.begin()
#
#     def rollback(self):
#         if self.session:
#             self.session.rollback()
#
#     def commit(self):
#         if self.session:
#             self.session.commit()
#
#
# class DbUtil:
#     """DB Util"""
#     # @staticmethod
#     # def get_db():
#     #     return DbAccess.get_instance()
#     #
#     # @staticmethod
#     # def close_db(db_agent):
#     #     if db_agent is not None:
#     #         db_agent.close()
#     #
#     # @classmethod
#     # def db_rollback(cls, db_agent, function_name):
#     #     try:
#     #         db_agent.rollback()
#     #     except Exception as ex:
#     #         cls.log_error(function_name, ex)
#     #
#     # @staticmethod
#     # def is_connection_valid(exception):
#     #     """
#     #     Check if error type is connection error
#     #     Transaction error is treated as connection error。
#     #     :type exception: OperationalError/DBAPIError/DBAccessError
#     #     :param exception: エラー
#     #         OperationalError: query error
#     #         DBAPIError：other error
#     #         DBAccessError: transaction error
#     #     :rtype: bool
#     #     :return: True: not connection error, False: connection error
#     #     """
#     #     if type(exception) == OperationalError:
#     #         # https://dev.mysql.com/doc/refman/5.7/en/error-messages-client.html#
#     #         # Connection error code
#     #         return exception.orig.args[0] not in (2006, 2013, 2014, 2045, 2055)
#     #     # all none query error is treated as connection error
#     #     return not getattr(exception, 'connection_invalidated', True)
#
#     @staticmethod
#     def is_key_duplicated_error(exception):
#         """
#         Check if error type is primary key duplicated error
#         :type exception: IntegrityError
#         :param exception: error
#         :rtype: bool
#         :return: True: primary key duplicated error, False: primary key duplicated error
#         """
#         if type(exception) == IntegrityError:
#             # check error code
#             return exception.orig.args[0] == str(23000)
#         # all none query error is treated as connection error
#         return False
#
#     @classmethod
#     def log_error(cls, function_name, exception):
#         raise NotImplementedError()
