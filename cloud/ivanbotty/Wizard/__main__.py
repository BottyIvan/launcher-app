#!/usr/bin/env python3
"""Entry point for the Welcome Wizard application.

This module provides a standalone entry point for launching the Welcome Wizard
directly without checking user preferences.
"""
import sys

import gi

gi.require_version("Gtk", "4.0")

from cloud.ivanbotty.utils import initialize_app, setup_logging
from cloud.ivanbotty.Wizard.app import WelcomeWizard


def main() -> int:
    """Initialize and run the Welcome Wizard.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    logger = setup_logging()
    
    # Initialize application resources and database
    if not initialize_app("Welcome Wizard"):
        return 1
    
    # Create and run the Welcome Wizard
    try:
        app = WelcomeWizard(app='cloud.ivanbotty.Wizard')
        app.run()
        return 0
    except Exception as e:
        logger.error(f"Failed to launch Welcome Wizard: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
