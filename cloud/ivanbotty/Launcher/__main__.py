#!/usr/bin/env python3
import gi

# Set the required GTK version
gi.require_version("Gtk", "4.0")
from gi.repository import Gio
import cloud.ivanbotty.database.sqlite3 as db
from cloud.ivanbotty.Launcher.app import App

def main():
    # Load and register application resources
    try:
        import os
        import sys
        
        # Try to find the resources file in different locations
        resource_paths = [
            # Direct execution from repository root
            "cloud/ivanbotty/Launcher/resources/resources.gresource",
            # Meson installation (in pkgdatadir)
            os.path.join(sys.prefix, "share", "launcher-app", "Launcher", "resources", "resources.gresource"),
            # Alternative Meson installation (in /usr/local)
            "/usr/local/share/launcher-app/Launcher/resources/resources.gresource",
            # Relative to this file
            os.path.join(os.path.dirname(__file__), "resources", "resources.gresource"),
        ]
        
        resource = None
        for path in resource_paths:
            if os.path.exists(path):
                resource = Gio.Resource.load(path)
                break
        
        if resource is None:
            print(f"Failed to load resources: resources.gresource not found")
            print(f"Tried paths: {resource_paths}")
            return
        
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
    app = App()
    app.run()

if __name__ == "__main__":
    # Entry point of the application
    main()
