import cloud.ivanbotty.database.sqlite3 as db
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Define constant for host prefix
HOST_PREFIX = "/run/host"

# Directories to search for .desktop application files
SYSTEM_DIRS = [
    Path("/usr/share/applications"),  # system applications
    Path(f"{HOST_PREFIX}/usr/share/applications"),  # host applications
    Path(f"{HOST_PREFIX}/var/lib/flatpak/exports/share/applications"),  # flatpak system-wide applications
    Path.home() / ".local/share/applications",  # user applications
    Path(f"{HOST_PREFIX}{Path.home()}/.local/share/applications"),  # user applications from host perspective
]

# Directories to search for icons
# Directories to search for icons
ICON_DIRS = [
    Path("/usr/share/icons"),  # system-wide icons
    Path("/usr/share/pixmaps"),  # system-wide pixmaps
    Path.home() / ".local/share/icons",  # user-specific icons
    Path.home() / ".icons",  # legacy user-specific icons
    Path(f"{HOST_PREFIX}/usr/share/icons"),  # host system-wide icons
    Path(f"{HOST_PREFIX}/usr/share/pixmaps"),  # host system-wide pixmaps
    Path(f"{HOST_PREFIX}{Path.home()}/.local/share/icons"),  # host user-specific icons
    Path(f"{HOST_PREFIX}{Path.home()}/.icons"),  # host legacy user-specific icons
    Path(f"{HOST_PREFIX}/var/lib/flatpak/app"),  # flatpak app icons
    Path(f"{HOST_PREFIX}/var/lib/flatpak/runtime"),  # flatpak runtime icons
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
        "margin_end": 8,
    },
    DEFAULT_STYLE: {
        "width": 800,
        "height": 540,
        "entry_width": 760,
        "entry_height": 48,
        "margin_top": 16,
        "margin_bottom": 16,
        "margin_start": 16,
        "margin_end": 16,
    },
}

# Retrieve the user's preferred UI style from the database.
# If the preference is not set or invalid, fall back to the default style.
try:
    pref = db.get_pref("layout", "default")
    PREFERENCES = pref if pref in UI_CONFS else "default"
except Exception:
    # On error (e.g., database unavailable), use the default style and log the issue.
    PREFERENCES = "default"
    logger.warning("Failed to get preferences, using default")

SYSTEM_PROMPT = (
    "You are a helpful assistant focused on concise, accurate answers. "
    "Respond only to the user's question, avoiding unnecessary details. "
    'Always reply in JSON format: {"response": "your answer"}. '
    "Example questions: What is the capital of France? How do I create a virtual environment in Python? "
    'Example response: {"response": "Paris is the capital of France."} '
    "Keep responses brief and relevant."
)
