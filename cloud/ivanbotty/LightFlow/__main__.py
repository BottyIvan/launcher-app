#!/usr/bin/env python3
"""Main entry point for the LightFlow application.

This module serves as the entry point for the LightFlow application. It handles
initialization and decides whether to show the welcome wizard or the main application
based on user preferences.
"""
import sys

import gi

gi.require_version("Gtk", "4.0")

from cloud.ivanbotty.LightFlow.config.config import (should_show_onboarding,
                                                    mark_onboarding_complete)
from cloud.ivanbotty.LightFlow.app import App
from cloud.ivanbotty.utils import configure_cli, initialize_app, setup_logging
from cloud.ivanbotty.Wizard.app import WelcomeWizard


def main() -> int:
    """Initialize and run the application.

    Returns:
        Exit code (0 for success, 1 for failure)
    """

    try:
        args = configure_cli(version="0.0.1")
        logger = setup_logging(args.log_level)
    except Exception as e:
        print(f"Error parsing command-line arguments: {e}", file=sys.stderr)
        return 1

    # Initialize application resources and database
    if not initialize_app("LightFlow"):
        return 1

    # Decide which application to launch based on user preferences
    try:
        logger.info("Starting LightFlow Application")
        logger.debug(f"show_welcome_wizard preference: {should_show_onboarding()}")
        if should_show_onboarding():
            app = WelcomeWizard(app="cloud.ivanbotty.Wizard")
            logger.info("Launching Welcome Wizard")
        else:
            app = App(app="cloud.ivanbotty.LightFlow")
            logger.info("Launching Main Application")

        app.run()
        return 0
    except Exception as e:
        logger.error(f"Failed to launch application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
