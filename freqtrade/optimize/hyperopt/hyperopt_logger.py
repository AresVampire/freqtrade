import logging
from logging.handlers import QueueHandler
from multiprocessing import Queue, current_process
from queue import Empty


logger = logging.getLogger(__name__)


def logging_mp_setup(log_queue: Queue, verbosity: int):
    """
    Setup logging in a child process.
    Must be called in the child process before logging.
    log_queue MUST be passed to the child process via inheritance
        Which essentially means that the log_queue must be a global, created in the same
        file as Parallel is initialized.
    """
    current_proc = current_process().name
    if current_proc != "MainProcess":
        h = QueueHandler(log_queue)
        root = logging.getLogger()
        root.setLevel(verbosity)
        root.addHandler(h)


def logging_mp_handle(q: Queue):
    """
    Handle logging in a child process.
    Must be called in the child process after logging.
    """

    try:
        while True:
            record = q.get(block=False)
            # logger1 = logging.getLogger(record.name)
            if record is None:
                break
            logger.handle(record)

    except Empty:
        logger.info("empty")
        # print("empty")
        pass
