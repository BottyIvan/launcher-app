"""Thread management utilities for background task execution.

This module provides utilities for running functions in separate threads,
allowing the UI to remain responsive during long-running operations.
"""

import logging
import threading
from typing import Any, Callable, List, Tuple

logger = logging.getLogger(__name__)


class ThreadManager:
    """Manager for running functions in separate threads.

    Allows launching services/extensions without blocking the UI.
    """

    def run_in_thread(self, target: Callable, *args: Any, **kwargs: Any) -> threading.Thread:
        """Run the target function in a new daemon thread.

        Args:
            target: Function to execute in the thread
            *args: Positional arguments for the target function
            **kwargs: Keyword arguments for the target function

        Returns:
            The created Thread object
        """
        logger.debug(f"Running function in separate thread: target={target.__name__}")
        thread = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread

    def run_multiple(self, targets: List[Tuple[Callable, tuple, dict]]) -> List[threading.Thread]:
        """Run multiple functions in parallel threads.

        Args:
            targets: List of tuples (function, args, kwargs)

        Returns:
            List of created Thread objects
        """
        threads = []
        for target, args, kwargs in targets:
            logger.debug(f"Running function in separate thread: target={target.__name__}")
            t = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
            t.start()
            threads.append(t)
        return threads
