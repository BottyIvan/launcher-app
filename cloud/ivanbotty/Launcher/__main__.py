#!/usr/bin/env python3
"""Main entry point for the Launcher application.

This module serves as the entry point for the Launcher application. It handles
initialization and decides whether to show the welcome wizard or the main application
based on user preferences.
"""
import sys

import gi

gi.require_version("Gtk", "4.0")

import cloud.ivanbotty.database.sqlite3 as db
from cloud.ivanbotty.Launcher.app import App
from cloud.ivanbotty.utils import initialize_app, setup_logging
from cloud.ivanbotty.Wizard.app import WelcomeWizard


def main() -> int:
    """Initialize and run the application.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    logger = setup_logging()

    # Initialize application resources and database
    if not initialize_app("Launcher"):
        return 1

    # Decide which application to launch based on user preferences
    try:
        if db.get_pref("show_welcome_wizard", True) is True:
            db.set_pref("show_welcome_wizard", False)
            app = WelcomeWizard(app="cloud.ivanbotty.Wizard")
            logger.info("Launching Welcome Wizard")
        else:
            app = App(app="cloud.ivanbotty.Launcher")
            logger.info("Launching Main Application")

        app.run()
        return 0
    except Exception as e:
        logger.error(f"Failed to launch application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
