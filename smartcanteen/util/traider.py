from datetime import datetime, timedelta, date
from multiprocessing import Process, Queue
from time import sleep

from config.config import TimeRequest
from smartcanteen.util.exchange_process import ExchangeProcess
from smartcanteen.util.log_agent import LoggerAgent
import ccxt


class TraderProcess:
    queue_data = None
    process = None
    logger = None
    time_request = TimeRequest.GET_REQUEST
    stop_flag = False

    @classmethod
    def start(cls, coin, exchangFirst, exchangSecond):
        logger = LoggerAgent.get_instance()
        logger.info("===============================================")
        logger.info("==============  START SYNC DATA ===============")
        logger.info("===============================================")
        cls.__init()
        cls.__do_trader()

        logger.info("================END SYNC DATA  ==============")

    @classmethod
    def __init(cls):
        pass

    @classmethod
    def __do_trader(cls):
        queue_first = Queue()
        process_get = ExchangeProcess(queue_first)
        process_get.start()

        queue_second = Queue()
        process_send = ExchangeProcess(queue_second)
        process_send.start()

        process_get.stop()
        process_send.stop()
