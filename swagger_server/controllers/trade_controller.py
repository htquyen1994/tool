import connexion
import six

from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.trade_request import TradeRequest  # noqa: E501
from swagger_server.models.trade_response import TradeResponse  # noqa: E501
from swagger_server import util


def init_post(InitTrade):  # noqa: E501
    """Init trade post

    Do init trade # noqa: E501

    :param InitTrade: Parameter Init trade
    :type InitTrade: dict | bytes

    :rtype: TradeResponse
    """
    if connexion.request.is_json:
        InitTrade = TradeRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
