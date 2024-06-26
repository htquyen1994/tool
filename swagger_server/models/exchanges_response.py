# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ExchangesResponse(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, coin_list: List[str]=None):  # noqa: E501
        """ExchangesResponse - a model defined in Swagger

        :param coin_list: The coin_list of this ExchangesResponse.  # noqa: E501
        :type coin_list: List[str]
        """
        self.swagger_types = {
            'coin_list': List[str]
        }

        self.attribute_map = {
            'coin_list': 'coin_list'
        }

        self._coin_list = coin_list

    @classmethod
    def from_dict(cls, dikt) -> 'ExchangesResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ExchangesResponse of this ExchangesResponse.  # noqa: E501
        :rtype: ExchangesResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def coin_list(self) -> List[str]:
        """Gets the coin_list of this ExchangesResponse.


        :return: The coin_list of this ExchangesResponse.
        :rtype: List[str]
        """
        return self._coin_list

    @coin_list.setter
    def coin_list(self, coin_list: List[str]):
        """Sets the coin_list of this ExchangesResponse.


        :param coin_list: The coin_list of this ExchangesResponse.
        :type coin_list: List[str]
        """

        self._coin_list = coin_list
