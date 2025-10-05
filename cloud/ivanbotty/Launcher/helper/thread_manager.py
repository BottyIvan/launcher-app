import threading

class ThreadManager:
    """
    Manager for running functions in separate threads.
    Allows launching services/extensions without blocking the UI.
    """

    def run_in_thread(self, target, *args, **kwargs):
        """
        Runs the target function in a new thread.
        """
        print(f"Running {target.__name__} in a separate thread.")
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
            print(f"Running {target.__name__} in a separate thread.")
            t = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
            t.start()
            threads.append(t)
        return threads