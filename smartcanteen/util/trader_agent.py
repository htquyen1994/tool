import multiprocessing
from multiprocessing.queues import Queue

from smartcanteen.util.exchange_process import ExchangeProcess
from smartcanteen.util.log_agent import LoggerAgent

def initialize():
    LoggerAgent.init_finished = True
    print("__initialize")


class TraderAgent:
    __instance = None
    __worker_process = None
    stop_flag = False

    # Initialization flag
    init_finished = False
    logger = None

    @staticmethod
    def get_instance():
        if TraderAgent.__instance is None:
            _instance = TraderAgent("TradeProcess")
        return TraderAgent.__instance

    def __init__(self, proc_name):
        try:
            ctx = multiprocessing.get_context()
            print(multiprocessing)
            super(TraderAgent, self).__init__(ctx=ctx)
            TraderAgent.__instance = self
            self.proc_name = proc_name
            TraderAgent.__worker_process = None
            self.logger = LoggerAgent.get_instance()

        except TraderAgent as ex:
            print("TraderAgent.__init__:{}".format(ex.__str__()))

    def initialize(self, ):

    def __stop_worker(self):
        if TraderAgent.__worker_process is not None:
            self.logger.info("------------------------------------------------")
            self.logger.info("------------------ STOP PROCESS ----------------")
            self.logger.info("------------------------------------------------")
            TraderAgent.__worker_process.join()
            TraderAgent.__worker_process = None

    def start(self):
        self.logger.info("------------------------------------------------")
        self.logger.info("----------------- START PROCESS ----------------")
        self.logger.info("------------------------------------------------")
        self.__start_worker()

    def __start_worker(self):
        """Start worker process. Worker process get log form queue the save to file
        :return: -
        """
        if TraderAgent.__worker_process is None:
            print("__start_worker init process")
            TraderAgent.__worker_process = multiprocessing.Process(
                target=self.worker_handler,
                args=(self, self.proc_name)
            )

            TraderAgent.__worker_process.daemon = False
            TraderAgent.__worker_process.start()

    def worker_handler(self, proc_name):
            """
            Worker process function
            :type queue: multiprocessing.queues.Queue
            :param queue: (multiprocessing.queues.Queue) log queue
            :param proc_name: process name
            :return: -
            """
            try:
                if not TraderAgent.init_finished:
                    # Initialize
                    print("LoggerAgent: not LoggerAgent.init_finished")
                    initialize()

                # Get log instance
                primary_queue = Queue()
                primary_exchange = ExchangeProcess(primary_queue)
                secondary_queue = Queue()
                secondary_exchange = ExchangeProcess(secondary_queue)
                primary_exchange.start()
                secondary_exchange.start()

                while True:
                    primary_msg = primary_queue.get()
                    secondary_msg = secondary_queue.get()
                    # Finish message

            except Exception as ex:
                print("TraderAgent.worker_handler::".format(ex.__str__()))

        