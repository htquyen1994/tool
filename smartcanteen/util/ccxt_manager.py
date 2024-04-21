import ccxt

from config.config import ExchangesCode


def init_cctx_exchange(exchange):
    ccxt_exchange = None
    exchange_code = exchange.code
    param = {'apiKey': exchange.private_key, 'secret': exchange.secret_key}
    if exchange_code == ExchangesCode.BINANCE:
        ccxt_exchange = ccxt.binance(param)
    elif exchange_code == ExchangesCode.OKEX:
        param['password'] = exchange.password
        ccxt_exchange = ccxt.okx(param)
    elif exchange_code == ExchangesCode.GATE:
        ccxt_exchange = ccxt.gate(param)
    elif exchange_code == ExchangesCode.HOUBI:
        ccxt_exchange = ccxt.huobi(param)
    elif exchange_code == ExchangesCode.BYBIT:
        ccxt_exchange = ccxt.bybit(param)
    elif exchange_code == ExchangesCode.KUCOIN:
        ccxt_exchange = ccxt.kucoin(param)
    elif exchange_code == ExchangesCode.BITGET:
        ccxt_exchange = ccxt.bitget(param)
    elif exchange_code == ExchangesCode.MEXC:
        ccxt_exchange = ccxt.mexc(param)
    return ccxt_exchange


class CcxtManager:
    __instance = None
    __primary_exchange = None
    __secondary_exchange = None
    __ccxt_primary = None
    __ccxt_secondary = None
    __coin_trade = None

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        if CcxtManager.__instance is None:
            _instance = CcxtManager()
        return CcxtManager.__instance

    def set_primary_exchange(self, exchange_info):
        self.__primary_exchange = exchange_info
        self.__ccxt_primary = init_cctx_exchange(exchange_info)

    def set_secondary_exchange(self, exchange_info):
        self.__secondary_exchange = exchange_info
        self.__ccxt_secondary = init_cctx_exchange(exchange_info)

    def get_exchange(self, is_primary):
        if is_primary:
            return self.__primary_exchange
        return self.__secondary_exchange

    def set_coin_trade(self, coin):
        self.__coin_trade = coin

    def get_ccxt(self, is_primary):
        if is_primary:
            return self.__ccxt_primary
        return self.__ccxt_secondary

    def get_coin_trade(self):
        return self.__coin_trade
