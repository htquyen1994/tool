# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.exchange_request import ExchangeRequest
from swagger_server import util


class TradeRequest(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, coin: str=None, primary_exchange: ExchangeRequest=None, secondary_exchange: ExchangeRequest=None, limit: int=None, simulated: int=None):  # noqa: E501
        """TradeRequest - a model defined in Swagger

        :param coin: The coin of this TradeRequest.  # noqa: E501
        :type coin: str
        :param primary_exchange: The primary_exchange of this TradeRequest.  # noqa: E501
        :type primary_exchange: ExchangeRequest
        :param secondary_exchange: The secondary_exchange of this TradeRequest.  # noqa: E501
        :type secondary_exchange: ExchangeRequest
        :param limit: The limit of this TradeRequest.  # noqa: E501
        :type limit: int
        :param simulated: The simulated of this TradeRequest.  # noqa: E501
        :type simulated: int
        """
        self.swagger_types = {
            'coin': str,
            'primary_exchange': ExchangeRequest,
            'secondary_exchange': ExchangeRequest,
            'limit': int,
            'simulated': int
        }

        self.attribute_map = {
            'coin': 'coin',
            'primary_exchange': 'primary_exchange',
            'secondary_exchange': 'secondary_exchange',
            'limit': 'limit',
            'simulated': 'simulated'
        }

        self._coin = coin
        self._primary_exchange = primary_exchange
        self._secondary_exchange = secondary_exchange
        self._limit = limit
        self._simulated = simulated

    @classmethod
    def from_dict(cls, dikt) -> 'TradeRequest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The TradeRequest of this TradeRequest.  # noqa: E501
        :rtype: TradeRequest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def coin(self) -> str:
        """Gets the coin of this TradeRequest.

        coin trade  # noqa: E501

        :return: The coin of this TradeRequest.
        :rtype: str
        """
        return self._coin

    @coin.setter
    def coin(self, coin: str):
        """Sets the coin of this TradeRequest.

        coin trade  # noqa: E501

        :param coin: The coin of this TradeRequest.
        :type coin: str
        """

        self._coin = coin

    @property
    def primary_exchange(self) -> ExchangeRequest:
        """Gets the primary_exchange of this TradeRequest.

        Exchange primary  # noqa: E501

        :return: The primary_exchange of this TradeRequest.
        :rtype: ExchangeRequest
        """
        return self._primary_exchange

    @primary_exchange.setter
    def primary_exchange(self, primary_exchange: ExchangeRequest):
        """Sets the primary_exchange of this TradeRequest.

        Exchange primary  # noqa: E501

        :param primary_exchange: The primary_exchange of this TradeRequest.
        :type primary_exchange: ExchangeRequest
        """

        self._primary_exchange = primary_exchange

    @property
    def secondary_exchange(self) -> ExchangeRequest:
        """Gets the secondary_exchange of this TradeRequest.

        Exchange secondary  # noqa: E501

        :return: The secondary_exchange of this TradeRequest.
        :rtype: ExchangeRequest
        """
        return self._secondary_exchange

    @secondary_exchange.setter
    def secondary_exchange(self, secondary_exchange: ExchangeRequest):
        """Sets the secondary_exchange of this TradeRequest.

        Exchange secondary  # noqa: E501

        :param secondary_exchange: The secondary_exchange of this TradeRequest.
        :type secondary_exchange: ExchangeRequest
        """

        self._secondary_exchange = secondary_exchange

    @property
    def limit(self) -> int:
        """Gets the limit of this TradeRequest.

        Litmit  # noqa: E501

        :return: The limit of this TradeRequest.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit: int):
        """Sets the limit of this TradeRequest.

        Litmit  # noqa: E501

        :param limit: The limit of this TradeRequest.
        :type limit: int
        """

        self._limit = limit

    @property
    def simulated(self) -> int:
        """Gets the simulated of this TradeRequest.

        simulated  # noqa: E501

        :return: The simulated of this TradeRequest.
        :rtype: int
        """
        return self._simulated

    @simulated.setter
    def simulated(self, simulated: int):
        """Sets the simulated of this TradeRequest.

        simulated  # noqa: E501

        :param simulated: The simulated of this TradeRequest.
        :type simulated: int
        """

        self._simulated = simulated