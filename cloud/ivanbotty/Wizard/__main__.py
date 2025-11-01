#!/usr/bin/env python3
import gi
import logging
import os
import sys

# Set the required GTK version
gi.require_version("Gtk", "4.0")
from gi.repository import Gio
import cloud.ivanbotty.database.sqlite3 as db
from cloud.ivanbotty.Wizard.blueprint_app import WelcomeWizard as App

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def find_wizard_resource_file():
    """
    Find the wizard-resources.gresource file in various possible locations.
    
    Returns:
        str or None: Path to the resource file if found, None otherwise.
    """
    PKGDATADIR = "launcher-app"
    RESOURCE_SUBDIR = "Wizard"
    RESOURCE_FILE = "wizard-resources.gresource"
    
    # Build the resource filename path
    resource_filename = os.path.join(RESOURCE_SUBDIR, RESOURCE_FILE)
    
    # Define possible search paths
    search_paths = [
        # Meson build directory (for testing)
        os.path.join("build", "cloud", "ivanbotty", "Wizard", RESOURCE_FILE),
        # Flatpak installation (in /app)
        os.path.join("/app", "share", PKGDATADIR, resource_filename),
        # Meson installation (in pkgdatadir using sys.prefix)
        os.path.join(sys.prefix, "share", PKGDATADIR, resource_filename),
        # Standard installation locations
        os.path.join("/usr", "share", PKGDATADIR, resource_filename),
        os.path.join("/usr", "local", "share", PKGDATADIR, resource_filename),
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            return path
    
    return None

def main():
    # Load and register Wizard UI resources
    try:
        resource_path = find_wizard_resource_file()
        
        if resource_path is None:
            logger.error(f"Failed to load wizard resources: wizard-resources.gresource not found")
            return
        
        logger.info(f"Loading wizard resources from: {resource_path}")
        resource = Gio.Resource.load(resource_path)
        Gio.resources_register(resource)
    except Exception as e:
        logger.error(f"Failed to load wizard resources: {e}")
        return
    
    # Initialize the SQLite3 database
    try:
        db.init_db()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return

    # Create and run the main application
    app = App(app='cloud.ivanbotty.Wizard')
    app.run()

if __name__ == "__main__":
    # Entry point of the application
    main()
