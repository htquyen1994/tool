from datetime import time
from threading import Thread
from time import sleep

from smartcanteen.util.ccxt_manager import CcxtManager
from smartcanteen.util.log_agent import LoggerAgent


class ExchangeThread:
    thread = None
    logger = None
    __is_initialize = False
    __queue = None
    __is_primary = None

    __ccxt_manager = None
    __ccxt_exchange = None

    def __init__(self, queue, is_primary):
        self.is_running = False
        self.__is_initialize = False
        self.__queue = queue
        self.logger = LoggerAgent.get_instance()
        self.__is_primary = is_primary
        self.__ccxt_manager = CcxtManager.get_instance()
        self.__ccxt_exchange = self.__ccxt_manager.get_ccxt(self.__is_primary)

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
            self.thread.join()
            print("Job stopped successfully")
        else:
            print("Job is not running")

    def job_function(self):
        while self.is_running:
            try:
                param_object = {}
                orderbook = self.__ccxt_exchange.fetch_order_book(self.__ccxt_manager.get_coin_trade())
                param_object['order_book'] = orderbook

                balance = self.__ccxt_exchange.fetch_balance()
                param_object['balance'] = {}
                for currency, amount in balance['total'].items():
                    if (currency == "USDT") and (amount > 0):
                        param_object['balance']['amount_usdt'] = amount
                    if (currency == self.__ccxt_manager.get_coin_trade()) and (amount > 0):
                        param_object['balance']['amount_coin'] = amount
                self.__queue.put(param_object)
                print("ExchangeThread.job_function::"
                      + self.__ccxt_exchange.exchange_code
                      + " ====> ::".format(param_object['balance'].__str__()))
                sleep(10)

            except Exception as ex:
                sleep(10)
                print("ExchangeThread.job_function::".format(ex.__str__()))

