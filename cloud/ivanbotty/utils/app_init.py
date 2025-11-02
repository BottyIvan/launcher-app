"""Application initialization utilities.

This module provides shared functions for resource loading, database initialization,
and logging setup used by both Launcher and Wizard entry points.
"""

import argparse
import logging
from typing import Optional

try:
    import gi

    gi.require_version("Gtk", "4.0")
    from gi.repository import Gio

    GTK_AVAILABLE = True
except (ValueError, ImportError):
    # GTK4 not available - this is okay for testing
    GTK_AVAILABLE = False
    Gio = None

import cloud.ivanbotty.database.sqlite3 as db
from cloud.ivanbotty.common import find_resource_file, RESOURCE_FILE

def build_parser(version: Optional[str] = None) -> argparse.ArgumentParser:
    """Create and configure the argument parser for the Launcher application.

    Args:
        version: Optional application version string for the --version flag.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        description="Launcher App - flexible startup options for configuration, logging, and automation"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose logging for troubleshooting and development"
    )
    parser.add_argument(
        "--wizard",
        action="store_true",
        help="Launch the welcome wizard on startup for first-time setup"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Specify an alternative configuration file location"
    )
    parser.add_argument(
        "--search",
        type=str,
        help="Automatically perform a search with the provided query on startup"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=version if version else "Launcher App (version unknown)",
        help="Show application version and exit"
    )
    return parser

def parse_args(args=None, version: Optional[str] = None) -> argparse.Namespace:
    """Parse command-line arguments and set derived values.

    Args:
        args: Optional list of argument strings to parse (defaults to sys.argv).
        version: Optional application version string for the --version flag.

    Returns:
        Namespace with parsed arguments and computed log_level.
    """
    parser = build_parser(version)
    parsed = parser.parse_args(args)

    # Set log_level based on --debug flag
    parsed.log_level = logging.DEBUG if parsed.debug else logging.INFO
    return parsed

def configure_cli(version: Optional[str] = None) -> argparse.Namespace:
    """Parse CLI arguments and return the resulting namespace.

    Args:
        version: Optional application version string for the --version flag.

    Returns:
        Namespace with parsed arguments and computed log_level.
    """
    return parse_args(version=version)

def setup_logging(
    level: int = logging.INFO,
    format_string: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> logging.Logger:
    """Configure logging for the application.

    Args:
        level: Logging level (default: logging.INFO)
        format_string: Format string for log messages

    Returns:
        Logger instance for the calling module
    """
    logging.basicConfig(level=level, format=format_string)
    return logging.getLogger(__name__)


def load_resources() -> bool:
    """Load and register application resources.

    Returns:
        True if resources were loaded successfully, False otherwise
    """
    if not GTK_AVAILABLE:
        logger = logging.getLogger(__name__)
        logger.warning("GTK4 not available, skipping resource loading")
        return False

    logger = logging.getLogger(__name__)

    try:
        resource_path = find_resource_file()

        if resource_path is None:
            logger.error(f"Failed to load resources: {RESOURCE_FILE} not found")
            return False

        resource = Gio.Resource.load(resource_path)
        Gio.resources_register(resource)
        logger.info(f"Resources loaded successfully from {resource_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to load resources: {e}")
        return False


def initialize_database() -> bool:
    """Initialize the SQLite database.

    Returns:
        True if database was initialized successfully, False otherwise
    """
    logger = logging.getLogger(__name__)

    try:
        db.init_db()
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return False


def initialize_app(app_name: Optional[str] = None) -> bool:
    """Perform complete application initialization.

    This function sets up logging, loads resources, and initializes the database.

    Args:
        app_name: Optional name for the application (used in logging)

    Returns:
        True if all initialization steps succeeded, False otherwise
    """
    logger = setup_logging()

    if app_name:
        logger.info(f"Initializing {app_name}")

    if not load_resources():
        return False

    if not initialize_database():
        return False

    logger.info("Application initialization completed successfully")
    return True

