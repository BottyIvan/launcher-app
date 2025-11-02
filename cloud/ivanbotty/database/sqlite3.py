"""SQLite database management for Launcher application.

This module provides functions for managing user preferences, extensions,
and API keys using a SQLite database.
"""

import os
import sqlite3
from typing import Any, Dict, Optional

# Path to the SQLite database
DB_PATH = os.path.expanduser("~/.config/cloud.ivanbotty.Launcher/settings.db")


def init_db() -> None:
    """Initialize the database and create tables if they do not exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Table for user preferences
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS preferences (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """
    )
    # Table for installed extensions
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS extensions (
            id TEXT PRIMARY KEY,
            enabled BOOLEAN
        )
    """
    )
    # Table for API keys of external services
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS api_keys (
            service TEXT PRIMARY KEY,
            key TEXT
        )
    """
    )
    conn.commit()
    conn.close()


# ----- Preferences -----
def set_pref(key: str, value: Any) -> None:
    """Set a preference (key, value) in the database.

    Args:
        key: The preference key
        value: The preference value (will be converted to string)
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("REPLACE INTO preferences (key, value) VALUES (?, ?)", (key, str(value)))
    conn.commit()
    conn.close()


def get_pref(key: str, default: Any = None) -> Any:
    """Retrieve the value of a preference.

    Args:
        key: The preference key
        default: Default value if key not found

    Returns:
        The preference value if found, otherwise the default value
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT value FROM preferences WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else default


# ----- Extensions -----
def get_extension(ext_id: str) -> Optional[bool]:
    """Retrieve the enabled/disabled state of an extension by its ID.

    Args:
        ext_id: The extension identifier

    Returns:
        True if enabled, False if disabled, None if not found
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT enabled FROM extensions WHERE id=?", (ext_id,))
    row = c.fetchone()
    conn.close()
    return row[0] == 1 if row else None


def set_extension_enabled(ext_id: str, enabled: bool) -> None:
    """Enable or disable an extension.

    If the extension does not exist, it will be created.

    Args:
        ext_id: The extension identifier
        enabled: True to enable, False to disable
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.execute(
                "INSERT INTO extensions (id, enabled) VALUES (?, ?) "
                "ON CONFLICT(id) DO UPDATE SET enabled=excluded.enabled",
                (ext_id, int(enabled)),
            )
    finally:
        conn.close()


def get_extensions() -> Dict[str, bool]:
    """Return a dictionary with extension ID and enabled/disabled state.

    Returns:
        Dictionary mapping extension IDs to their enabled state
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, enabled FROM extensions")
    result = {row[0]: (row[1] == 1) for row in c.fetchall()}
    conn.close()
    return result


# ----- API Keys -----
def set_api_key(service: str, key: str) -> None:
    """Save the API key for a service.

    Args:
        service: The service name
        key: The API key
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("REPLACE INTO api_keys (service, key) VALUES (?, ?)", (service, key))
    conn.commit()
    conn.close()


def get_api_key(service: str) -> Optional[str]:
    """Retrieve the API key for a service.

    Args:
        service: The service name

    Returns:
        The API key if found, None otherwise
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT key FROM api_keys WHERE service=?", (service,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None
