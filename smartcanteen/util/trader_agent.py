import multiprocessing
from multiprocessing.queues import Queue
from time import sleep

from smartcanteen.util.exchange_process import ExchangeProcess
from smartcanteen.util.exchange_thread import ExchangeThread
from smartcanteen.util.log_agent import LoggerAgent


class TraderAgent:
    __instance = None
    __worker_process = None
    stop_flag = False

    # Initialization flag
    init_process_trade = False
    logger = None
    running_flag = False
    __coin_trade = None
    __primary_exchange = None
    __secondary_exchange = None
    __simulator = True

    @staticmethod
    def get_instance():
        if TraderAgent.__instance is None:
            _instance = TraderAgent("TradeProcess")
        return TraderAgent.__instance

    def __init__(self, proc_name):
        try:
            self.logger.info("------------------------------------------------")
            self.logger.info("----------------- START PROCESS ----------------")
            self.logger.info("------------------------------------------------")
            ctx = multiprocessing.get_context()
            print(multiprocessing)
            super(TraderAgent, self).__init__(ctx=ctx)
            TraderAgent.__instance = self
            self.proc_name = proc_name
            self.__coin_trade = None
            self.__primary_exchange = None
            self.__secondary_exchange = None
            TraderAgent.__worker_process = None
            self.logger = LoggerAgent.get_instance()
            self.__start_worker()

        except TraderAgent as ex:
            print("TraderAgent.__init__:{}".format(ex.__str__()))

    def __stop_worker(self):
        if TraderAgent.__worker_process is not None:
            self.logger.info("------------------------------------------------")
            self.logger.info("------------------ STOP PROCESS ----------------")
            self.logger.info("------------------------------------------------")
            TraderAgent.__worker_process.join()
            TraderAgent.__worker_process = None

    def __start_worker(self):
        if TraderAgent.__worker_process is None:
            print("__start_worker init process")
            TraderAgent.__worker_process = multiprocessing.Process(target=self.worker_handler)

            TraderAgent.__worker_process.daemon = False
            TraderAgent.__worker_process.start()

    def set_config_trade(self, primary, secondary, coin, simulator):
        self.__primary_exchange = primary
        self.__secondary_exchange = secondary
        self.__coin_trade = coin
        self.__simulator = simulator

    def start_trade(self):
        self.logger.info("------------------------------------------------")
        self.logger.info("----------------- START TRADE ----------------")
        self.logger.info("------------------------------------------------")
        self.running_flag = True

    def stop_trade(self):
        self.logger.info("------------------------------------------------")
        self.logger.info("----------------- START TRADE ----------------")
        self.logger.info("------------------------------------------------")
        self.running_flag = False

    def worker_handler(self):
        try:

            while True:
                if not self.running_flag:
                    print("Process sleeping...")
                    sleep(10)
                else:
                    primary_queue = Queue()
                    secondary_queue = Queue()
                    while self.running_flag:
                        if not self.init_process_trade:
                            primary_exchange = ExchangeThread(primary_queue, self.__primary_exchange)
                            secondary_exchange = ExchangeThread(secondary_queue, self.__secondary_exchange)
                            primary_exchange.start_job(primary_queue)
                            secondary_exchange.start_job(secondary_queue)
                            self.init_process_trade = True

                        if not primary_queue.empty() and not secondary_queue.empty():
                            primary_msg = primary_queue.get()
                            secondary_msg = secondary_queue.get()

                            # primary exchange
                            primary_buy_price = primary_msg['order_book']['bids'][0][0]
                            primary_sell_price = primary_msg['order_book']['asks'][0][0]
                            primary_buy_quantity = primary_msg['order_book']['bids'][0][1]
                            primary_sell_quantity = primary_msg['order_book']['asks'][0][1]
                            primary_balance = primary_msg['balance']

                            primary_amount_usdt = primary_balance['amount_usdt']
                            primary_amount_coin = primary_balance['amount_coin']

                            # secondary exchange
                            secondary_buy_price = secondary_msg['order_book']['bids'][0][0]
                            secondary_sell_price = secondary_msg['order_book']['asks'][0][0]
                            secondary_buy_quantity = secondary_msg['order_book']['bids'][0][1]
                            secondary_sell_quantity = secondary_msg['order_book']['asks'][0][1]
                            secondary_balance = secondary_msg['balance']
                            secondary_amount_usdt = secondary_balance['amount_usdt']
                            secondary_amount_coin = secondary_balance['amount_coin']

                            if primary_buy_price > 1.01 * secondary_sell_price:
                                quantity = min(
                                    min(
                                        primary_buy_price * primary_buy_quantity,
                                        secondary_sell_price * secondary_sell_quantity,
                                        primary_amount_usdt,
                                        secondary_amount_usdt) / primary_buy_price, primary_amount_coin, secondary_amount_coin)
                                binance_order = binance.create_limit_sell_order(self.__coin_trade, quantity, primary_buy_price)
                                okx_order = okx.create_limit_buy_order(self.__coin_trade, quantity, secondary_sell_price)


                            elif secondary_buy_price > 1.01 * primary_sell_price:
                                quantity = min(
                                    min(
                                        secondary_buy_price * secondary_buy_quantity,
                                        primary_sell_price * primary_sell_quantity,
                                        secondary_amount_usdt,
                                        primary_amount_usdt) / secondary_buy_price, secondary_amount_coin,
                                    primary_amount_coin)
                                binance_order = binance.create_limit_buy_order(self.__coin_trade, quantity,
                                                                                primary_sell_price)
                                okx_order = okx.create_limit_sell_order(self.__coin_trade, quantity,
                                                                       secondary_buy_price)

except Exception as ex:
            print("TraderAgent.worker_handler::".format(ex.__str__()))

        
