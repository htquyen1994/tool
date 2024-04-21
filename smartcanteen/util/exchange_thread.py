from datetime import time
from threading import Thread
from time import sleep

import ccxt

from config.config import ExchangesCode
from smartcanteen.util.log_agent import LoggerAgent


class ExchangeThread:
    thread = None
    logger = None
    __api_key = None
    __secret_key = None
    __exchange_code = None
    __coin = None
    __ccxt_exchange = None
    __is_initialize = False
    __queue = None

    def __init__(self, queue, api_key, secret_key, exchange_code, coin):
        self.is_running = False
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__exchange_code = exchange_code
        self.__is_initialize = False
        self.__queue = queue
        self.logger = LoggerAgent.get_instance()

    def start_job(self, queue):
        if not self.is_running:
            self.is_running = True
            self.thread = Thread(target=self.job_function)
            self.thread.start()
            print("Job started successfully")
        else:
            print("Job is already running")

    def stop_job(self):
        if self.is_running:
            self.is_running = False
            print("Job stopping...")
            # Đợi cho luồng kết thúc
            self.thread.join()
            print("Job stopped successfully")
        else:
            print("Job is not running")

    def job_function(self):

        if not self.__is_initialize:
            self.initialize(self.__exchange_code)
            self.__is_initialize = True

        while self.is_running:
            try:
                orderbook = self.__ccxt_exchange.fetch_order_book(self.__coin)
                self.__queue.put(orderbook)
                sleep(10)

            except Exception as ex:
                sleep(10)
                print("ExchangeThread.job_function::".format(ex.__str__()))

    def initialize(self, exchange_code):
        if exchange_code == ExchangesCode.BINANCE:
            self.__ccxt_exchange = ccxt.binance({
                'apiKey': self.__api_key,
                'secret': self.__secret_key,
            })
        elif exchange_code == ExchangesCode.OKEX:
            self.__ccxt_exchange = ccxt.okx({
                'apiKey': self.__api_key,
                'secret': self.__secret_key,
            })

        elif exchange_code == ExchangesCode.GATE:
            self.__ccxt_exchange = ccxt.gate({
                'apiKey': self.__api_key,
                'secret': self.__secret_key,
            })
        elif exchange_code == ExchangesCode.HOUBI:
            self.__ccxt_exchange = ccxt.huobi({
                'apiKey': self.__api_key,
                'secret': self.__secret_key,
            })

        elif exchange_code == ExchangesCode.BYBIT:
            self.__ccxt_exchange = ccxt.bybit({
                'apiKey': self.__api_key,
                'secret': self.__secret_key,
            })
        elif exchange_code == ExchangesCode.KUCOIN:
            self.__ccxt_exchange = ccxt.kucoin({
                'apiKey': self.__api_key,
                'secret': self.__secret_key,
            })

        elif exchange_code == ExchangesCode.BITGET:
            self.__ccxt_exchange = ccxt.bitget({
                'apiKey': self.__api_key,
                'secret': self.__secret_key,
            })
        elif exchange_code == ExchangesCode.MEXC:
            self.__ccxt_exchange = ccxt.mexc({
                'apiKey': self.__api_key,
                'secret': self.__secret_key,
            })