"""Common utilities for the launcher application."""
import os
import sys

# Constants for resource paths
PKGDATADIR = "launcher-app"
RESOURCE_SUBDIR = "Launcher/resources"
RESOURCE_FILE = "resources.gresource"


def find_resource_file():
    """
    Find the resources.gresource file in various possible locations.
    
    This function searches for the resource file in multiple locations to support
    both direct Python execution from the repository and Meson-based installations.
    
    Returns:
        str or None: Path to the resource file if found, None otherwise.
    """
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
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            return path
    
    return None
