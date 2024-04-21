# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class UserInfo(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, login_id: int=None, user_name: str=None):  # noqa: E501
        """UserInfo - a model defined in Swagger

        :param login_id: The login_id of this UserInfo.  # noqa: E501
        :type login_id: int
        :param user_name: The user_name of this UserInfo.  # noqa: E501
        :type user_name: str
        """
        self.swagger_types = {
            'login_id': int,
            'user_name': str
        }

        self.attribute_map = {
            'login_id': 'login_id',
            'user_name': 'user_name'
        }

        self._login_id = login_id
        self._user_name = user_name

    @classmethod
    def from_dict(cls, dikt) -> 'UserInfo':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UserInfo of this UserInfo.  # noqa: E501
        :rtype: UserInfo
        """
        return util.deserialize_model(dikt, cls)

    @property
    def login_id(self) -> int:
        """Gets the login_id of this UserInfo.

        Login id  # noqa: E501

        :return: The login_id of this UserInfo.
        :rtype: int
        """
        return self._login_id

    @login_id.setter
    def login_id(self, login_id: int):
        """Sets the login_id of this UserInfo.

        Login id  # noqa: E501

        :param login_id: The login_id of this UserInfo.
        :type login_id: int
        """

        self._login_id = login_id

    @property
    def user_name(self) -> str:
        """Gets the user_name of this UserInfo.

        User name  # noqa: E501

        :return: The user_name of this UserInfo.
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name: str):
        """Sets the user_name of this UserInfo.

        User name  # noqa: E501

        :param user_name: The user_name of this UserInfo.
        :type user_name: str
        """

        self._user_name = user_name
