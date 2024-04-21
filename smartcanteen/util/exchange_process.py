from multiprocessing import Process
from time import sleep

from config.config import TimeRequest
from smartcanteen.util.log_agent import LoggerAgent


class ExchangeProcess:
    queue_data = None
    process = None
    logger = None
    time_request = TimeRequest.GET_REQUEST
    stop_flag = False

    def __init__(self, queue):
        self.queue_data = queue
        self.logger = LoggerAgent.get_instance()

    def start(self):
        self.logger.info("------------------------------------------------")
        self.logger.info("------------ START PROCESS GET DATA ------------")
        self.logger.info("------------------------------------------------")

        process = Process(target=self.do_work, args=(self.queue_data, self.logger))
        process.start()

    def stop(self):
        self.stop_flag = True
        self.process.join()

    def do_work(self, queue, logger):
        while not self.stop_flag:
            try:
                sleep(1)
                get_info()
                # TODO
            except Exception as ex:
                logger.error("@@@@@@@@ Error request get data: {0}".format(ex))
                sleep(ExchangeProcess.time_request)


def get_info():
    sleep(1)