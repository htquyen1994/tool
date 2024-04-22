import connexion
import six

from smartcanteen.logic.exchange_logic import ExchangeLogic
from swagger_server.models.coins_request import CoinsRequest  # noqa: E501
from swagger_server.models.coins_response import CoinsResponse  # noqa: E501
from swagger_server.models.common_response import CommonResponse  # noqa: E501
from swagger_server.models.configure_trade_request import ConfigureTradeRequest  # noqa: E501
from swagger_server.models.configure_trade_response import ConfigureTradeResponse  # noqa: E501
from swagger_server.models.exchanges_response import ExchangesResponse  # noqa: E501
from swagger_server import util


def coins(coins):  # noqa: E501
    """Fetch all coins post

    Do Fetch all coins post # noqa: E501

    :param coins: Parameter Fetch market trade post
    :type coins: dict | bytes

    :rtype: CoinsResponse
    """
    if connexion.request.is_json:
        coins = CoinsRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def config(configuration):  # noqa: E501
    """Configuration trade post

    Do Configuration trade # noqa: E501

    :param configuration: Parameter Configuration trade
    :type configuration: dict | bytes

    :rtype: ConfigureTradeResponse
    """
    if connexion.request.is_json:
        configuration = ConfigureTradeRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return ExchangeLogic.configure_post(configuration)


def exchanges():  # noqa: E501
    """Fetch all exchange post

    Do Fetch all exchange post # noqa: E501


    :rtype: ExchangesResponse
    """
    return ExchangeLogic.exchanges_get()
