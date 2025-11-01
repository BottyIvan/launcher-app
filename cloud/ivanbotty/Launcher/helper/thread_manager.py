import threading
import logging

logger = logging.getLogger(__name__)

class ThreadManager:
    """
    Manager for running functions in separate threads.
    Allows launching services/extensions without blocking the UI.
    """

    def run_in_thread(self, target, *args, **kwargs):
        """
        Runs the target function in a new thread.
        """
        logger.debug(f"Running function in separate thread: target={target.__name__}")
        thread = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread

    def run_multiple(self, targets):
        """
        Runs multiple functions in parallel.
        targets: list of tuples (function, args, kwargs)
        """
        threads = []
        for target, args, kwargs in targets:
            logger.debug(f"Running function in separate thread: target={target.__name__}")
            t = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
            t.start()
            threads.append(t)
        return threads