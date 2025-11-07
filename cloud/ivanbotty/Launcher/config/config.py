import cloud.ivanbotty.database.sqlite3 as db
from pathlib import Path
import logging
import time

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
        "entry_height": 40,  # Slightly larger for better touch
        "margin_top": 10,
        "margin_bottom": 10,
        "margin_start": 10,
        "margin_end": 10,
        "progress_margin_top": 6,
        "progress_margin_bottom": 6,
        "icon_size": 32,  # Icon size in pixels
    },
    DEFAULT_STYLE: {
        "width": 850,  # Slightly wider for better content display
        "height": 580,  # Slightly taller for more results
        "entry_width": 810,
        "entry_height": 52,  # Larger for better accessibility
        "margin_top": 16,
        "margin_bottom": 16,
        "margin_start": 20,  # More breathing room
        "margin_end": 20,
        "progress_margin_top": 8,
        "progress_margin_bottom": 8,
        "icon_size": 32,  # Icon size in pixels
    },
}

# Animation and transition settings
# These can be adjusted by users via preferences or configuration files
ANIMATION_SETTINGS = {
    "enable_animations": True,  # Global animation toggle
    "transition_duration": 200,  # Duration in milliseconds for transitions
    "icon_hover_scale": 1.05,  # Scale factor for icon hover effect (if animations enabled)
}

# Category tag configuration
# Maps result types to Adwaita style classes for native theming
CATEGORY_TAG_STYLES = {
    "application": "accent",  # Uses system accent color (typically blue)
    "math": "success",  # Green tone
    "ai": "accent",  # Uses system accent color
    "command": "warning",  # Orange tone
    "file": "accent",  # Default accent
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

# Onboarding configuration helpers
def should_show_onboarding() -> bool:
    """Check if the onboarding wizard should be shown.
    
    Returns:
        bool: True if onboarding should be shown, False otherwise
    """
    try:
        return db.get_pref("show_welcome_wizard", True) is True
    except Exception:
        logger.warning("Failed to check onboarding preference, defaulting to True")
        return True

def mark_onboarding_complete() -> None:
    """Mark the onboarding wizard as complete."""
    try:
        db.set_pref("show_welcome_wizard", False)
        db.set_pref("onboarding_completed_at", str(int(time.time())))
        logger.info("Onboarding marked as complete")
    except Exception as e:
        logger.error(f"Failed to mark onboarding complete: {e}")

def reset_onboarding() -> None:
    """Reset the onboarding state to show it again on next launch."""
    try:
        db.set_pref("show_welcome_wizard", True)
        logger.info("Onboarding reset - will show on next launch")
    except Exception as e:
        logger.error(f"Failed to reset onboarding: {e}")
