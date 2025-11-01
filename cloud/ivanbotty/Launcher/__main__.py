#!/usr/bin/env python3
import gi
import logging

# Set the required GTK version
gi.require_version("Gtk", "4.0")
from gi.repository import Gio
import cloud.ivanbotty.database.sqlite3 as db
from cloud.ivanbotty.Launcher.app import App
from cloud.ivanbotty.common import find_resource_file, RESOURCE_FILE
from cloud.ivanbotty.Wizard.app import WelcomeWizard

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Load and register application resources
    try:
        resource_path = find_resource_file()
        
        if resource_path is None:
            logger.error(f"Failed to load resources: {RESOURCE_FILE} not found")
            return
        
        resource = Gio.Resource.load(resource_path)
        Gio.resources_register(resource)
    except Exception as e:
        logger.error(f"Failed to load resources: {e}")
        return
    
    # Initialize the SQLite3 database
    try:
        db.init_db()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return

    # Create and run the main application
    if db.get_pref("show_welcome_wizard", True):
        app = WelcomeWizard(app='cloud.ivanbotty.Wizard')
    else:
        app = App(app='cloud.ivanbotty.Launcher')
    app.run()

if __name__ == "__main__":
    # Entry point of the application
    main()
