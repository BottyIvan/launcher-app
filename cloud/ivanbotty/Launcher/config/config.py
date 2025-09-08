import cloud.ivanbotty.database.sqlite3 as db
from pathlib import Path

# Directories to search for .desktop application files
SYSTEM_DIRS = [
    Path("/usr/share/applications"),                                # system applications
    Path("/run/host/usr/share/applications"),                       # host applications
    Path("/run/host/var/lib/flatpak/exports/share/applications"),   # flatpak system-wide applications
    Path.home() / ".local/share/applications",                      # user applications
    Path("/run/host" + str(Path.home()) + "/.local/share/applications")  # user applications from host perspective
]

# Directories to search for icons
ICON_DIRS = [
    Path("/usr/share/icons"),                                        # system-wide icon themes
    Path("/usr/share/pixmaps"),                                      # legacy system icons
    Path.home() / ".local/share/icons",                               # user icons
    Path.home() / ".icons",                                           # old user icons path
    Path("/var/lib/flatpak/app"),                                     # Flatpak app icons (system)
    Path("/run/host/var/lib/flatpak/app"),                            # Flatpak app icons (host)
    Path("/var/lib/flatpak/runtime")                                  # Flatpak runtime icons
]

ALL_APP_DIRS = SYSTEM_DIRS

# Define style names
COMPACT_STYLE = "compact"
DEFAULT_STYLE = "default"

# UI configuration for each style
UI_CONFS = {
    COMPACT_STYLE: {
        "width": 700,
        "height": 400,
        "entry_width": 660,
        "entry_height": 36,
        "margin_top": 8,
        "margin_bottom": 8,
        "margin_start": 8,
        "margin_end": 8
    },
    DEFAULT_STYLE: {
        "width": 800,
        "height": 540,
        "entry_width": 760,
        "entry_height": 48,
        "margin_top": 16,
        "margin_bottom": 16,
        "margin_start": 16,
        "margin_end": 16
    }
}

# Retrieve the user's preferred UI style from the database.
# If the preference is not set or invalid, fall back to the default style.
try:
    pref = db.get_pref("layout", "default")
    PREFERENCES = pref if pref in UI_CONFS else "default"
except Exception:
    # On error (e.g., database unavailable), use the default style and log the issue.
    PREFERENCES = "default"
    print("Failed to get preferences, using default.")

SYSTEM_PROMPT = (
    "You are a helpful assistant focused on concise, accurate answers. "
    "Respond only to the user's question, avoiding unnecessary details. "
    "Always reply in JSON format: {\"response\": \"your answer\"}. "
    "Example questions: What is the capital of France? How do I create a virtual environment in Python? "
    "Example response: {\"response\": \"Paris is the capital of France.\"} "
    "Keep responses brief and relevant."
)
