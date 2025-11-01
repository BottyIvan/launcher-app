#!/usr/bin/env python3
import gi

# Set the required GTK version
gi.require_version("Gtk", "4.0")
from gi.repository import Gio
import cloud.ivanbotty.database.sqlite3 as db
from cloud.ivanbotty.Wizard.app import WelcomeWizard as App

# Constants for resource paths (Wizard uses Launcher's resources)
PKGDATADIR = "launcher-app"
RESOURCE_SUBDIR = "Launcher/resources"
RESOURCE_FILE = "resources.gresource"

def find_resource_file():
    """Find the resources.gresource file in various possible locations."""
    import os
    import sys
    
    # Build the resource filename path
    resource_filename = os.path.join(RESOURCE_SUBDIR, RESOURCE_FILE)
    
    # Define possible search paths
    search_paths = [
        # Direct execution from repository root
        os.path.join("cloud", "ivanbotty", resource_filename),
        # Meson installation (in pkgdatadir)
        os.path.join(sys.prefix, "share", PKGDATADIR, resource_filename),
        # Alternative Meson installation (in /usr/local)
        os.path.join("/usr", "local", "share", PKGDATADIR, resource_filename),
        # Relative to Launcher module (one level up from Wizard)
        os.path.join(os.path.dirname(__file__), "..", "Launcher", "resources", RESOURCE_FILE),
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            return path
    
    return None

def main():
    # Load and register application resources
    try:
        resource_path = find_resource_file()
        
        if resource_path is None:
            print(f"Failed to load resources: {RESOURCE_FILE} not found")
            return
        
        resource = Gio.Resource.load(resource_path)
        Gio.resources_register(resource)
    except Exception as e:
        print(f"Failed to load resources: {e}")
        return
    
    # Initialize the SQLite3 database
    try:
        db.init_db()
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        return

    # Create and run the main application
    app = App(app='cloud.ivanbotty.Wizard')
    app.run()

if __name__ == "__main__":
    # Entry point of the application
    main()
