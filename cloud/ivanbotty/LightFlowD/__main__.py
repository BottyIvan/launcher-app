#!/usr/bin/env python3
"""LightFlowD daemon - background service for application indexing and caching.

This daemon runs in the background, periodically scanning for applications
and maintaining a cache for instant UI startup. It provides a D-Bus interface
for the UI to query cache status and receive progress updates.
"""

import sys
import time
import os
import json
import logging
import argparse
import signal

try:
    from gi.repository import GLib
    GLIB_AVAILABLE = True
except ImportError:
    GLIB_AVAILABLE = False
    GLib = None

from cloud.ivanbotty.LightFlow.services.applications_service import ApplicationsService
from cloud.ivanbotty.LightFlowD.dbus_service import LightFlowDDBusService

CACHE_PATH = os.path.expanduser("~/.cache/cloud.ivanbotty.LightFlow/applications_cache.json")
SCAN_INTERVAL = 60

logger = logging.getLogger(__name__)


def setup_logging(debug: bool = False) -> None:
    """Configure logging for the daemon.

    Args:
        debug: Enable debug logging if True
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def ensure_cache_dir_exists(path: str) -> None:
    """Ensure the cache directory exists.

    Args:
        path: Path to the cache file
    """
    cache_dir = os.path.dirname(path)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        logger.debug("Created cache directory: %s", cache_dir)


def update_cache(service: ApplicationsService, dbus_service=None) -> int:
    """Update the cache file with the list of applications.

    Args:
        service: ApplicationsService instance
        dbus_service: Optional D-Bus service for progress updates

    Returns:
        Number of applications cached
    """
    try:
        if dbus_service:
            dbus_service.set_indexing_state(True)
            dbus_service.update_indexing_progress(0.0, 0)

        store = service.load_applications()
        apps = [model.to_dict() for model in store]
        apps_count = len(apps)

        if dbus_service:
            dbus_service.update_indexing_progress(0.5, apps_count)

        ensure_cache_dir_exists(CACHE_PATH)
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(apps, f, indent=2, ensure_ascii=False)

        if dbus_service:
            dbus_service.update_indexing_progress(1.0, apps_count)
            dbus_service.set_indexing_state(False)
            dbus_service.emit_cache_updated(apps_count)

        logger.info("Cache updated with %d applications.", apps_count)
        return apps_count

    except Exception as e:
        logger.exception("Error updating the cache: %s", e)
        if dbus_service:
            dbus_service.set_indexing_state(False)
        return 0


def run_daemon(debug: bool = False, daemonize: bool = False) -> int:
    """Run the daemon service.

    Args:
        debug: Enable debug logging
        daemonize: Run as a background daemon

    Returns:
        Exit code
    """
    setup_logging(debug)

    if daemonize and os.name == 'posix':
        # Simple daemonization for Unix-like systems
        try:
            pid = os.fork()
            if pid > 0:
                # Parent process exits
                logger.info(f"Daemon started with PID {pid}")
                sys.exit(0)
        except OSError as e:
            logger.error(f"Fork failed: {e}")
            return 1

    # Initialize services
    service = ApplicationsService()

    # Start D-Bus service if available
    dbus_service = None
    if GLIB_AVAILABLE:
        try:
            dbus_service = LightFlowDDBusService(CACHE_PATH)
            if dbus_service.start():
                logger.info("D-Bus service started successfully")
            else:
                logger.warning("D-Bus service failed to start, continuing without it")
                dbus_service = None
        except Exception as e:
            logger.warning(f"Could not start D-Bus service: {e}")
            dbus_service = None
    else:
        logger.warning("GLib not available, D-Bus service disabled")

    # Set up signal handlers for graceful shutdown
    shutdown_requested = [False]

    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        shutdown_requested[0] = True

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initial cache update
    logger.info("LightFlowD daemon started. Scanning every %d seconds.", SCAN_INTERVAL)
    update_cache(service, dbus_service)

    # Main loop
    try:
        while not shutdown_requested[0]:
            time.sleep(SCAN_INTERVAL)
            if not shutdown_requested[0]:
                update_cache(service, dbus_service)
    except KeyboardInterrupt:
        logger.info("Service manually interrupted.")
    finally:
        # Clean up
        if dbus_service:
            dbus_service.stop()
        logger.info("Daemon stopped")

    return 0


def main() -> int:
    """Main entry point for the daemon.

    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        description="LightFlowD daemon - background application indexing service"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    parser.add_argument(
        "--daemonize",
        action="store_true",
        help="Run as a background daemon"
    )

    args = parser.parse_args()
    return run_daemon(debug=args.debug, daemonize=args.daemonize)


if __name__ == "__main__":
    sys.exit(main())
