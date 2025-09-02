#!/usr/bin/env python3
import gi

# Set the required GTK version
gi.require_version("Gtk", "4.0")
from gi.repository import Gio
from cloud.ivanbotty.database.sqlite3 import init_db
from cloud.ivanbotty.Launcher.app import App

def main():
    # Load and register application resources
    try:
        resource = Gio.Resource.load("cloud/ivanbotty/Launcher/resources/resources.gresource")
        Gio.resources_register(resource)
    except Exception as e:
        print(f"Failed to load resources: {e}")
        return
    
    # Initialize the SQLite3 database
    try:
        init_db()
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        return

    # Create and run the main application
    app = App()
    app.run()

if __name__ == "__main__":
    # Entry point of the application
    main()
