from smartcanteen.util.ccxt_manager import CcxtManager
from smartcanteen.util.common import Util
from smartcanteen.util.const import ResponseMessage
from smartcanteen.util.trader_agent import TraderAgent
from swagger_server.models import ConfigureTradeResponse, CommonResponse, ExchangesResponse


class ExchangeLogic:
    @classmethod
    @require_authenticate
    @Util.system_error_handler
    def configure_post(cls, configure):
        try:
            primary_exchange = configure.primary_exchange
            secondary_exchange = configure.secondary_exchange
            limit = configure.limit
            simulated = configure.limit
            coin = configure.coin
            TraderAgent.get_instance().set_config_trade(primary_exchange, secondary_exchange, coin, simulated)
            resp = configure
            return resp, ResponseMessage.Success.http_code
        except Exception as ex:
            print("ExchangeLogic.configure_post::".format(ex.__str__()))

    @classmethod
    @require_authenticate
    @Util.system_error_handler
    def start_post(cls):
        try:
            TraderAgent.get_instance().start_trade()
            resp = CommonResponse()
            return resp, ResponseMessage.Success.http_code
        except Exception as ex:
            print("ExchangeLogic.start_post::".format(ex.__str__()))

    @classmethod
    @require_authenticate
    @Util.system_error_handler
    def stop_post(cls):
        try:
            TraderAgent.get_instance().stop_trade()
            resp = CommonResponse()
            return resp, ResponseMessage.Success.http_code
        except Exception as ex:
            print("ExchangeLogic.stop_post::".format(ex.__str__()))

    @classmethod
    @require_authenticate
    @Util.system_error_handler
    def exchanges_get(cls):
        try:
            exchanges = CcxtManager.get_instance().get_exchanges_available()
            resp = ExchangesResponse()
            resp.coin_list = exchanges
            return resp, ResponseMessage.Success.http_code
        except Exception as ex:
            print("ExchangeLogic.stop_post::".format(ex.__str__()))