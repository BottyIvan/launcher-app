"""SQLite database management for LightFlow application.

This module provides functions for managing user preferences, extensions,
and API keys using a SQLite database.
"""

import os
import sqlite3
from typing import Any, Dict, Optional
from contextlib import contextmanager
import threading

# Path to the SQLite database
DB_PATH = os.path.expanduser("~/.config/cloud.ivanbotty.LightFlow/settings.db")

# Thread-local storage for connections
_local = threading.local()


def _get_connection() -> sqlite3.Connection:
    """Get or create a thread-local database connection.

    Returns:
        sqlite3.Connection: Thread-local database connection
    """
    if not hasattr(_local, 'connection') or _local.connection is None:
        _local.connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    else:
        # Check if connection is still valid
        try:
            _local.connection.execute("SELECT 1")
        except sqlite3.ProgrammingError:
            # Connection was closed, create a new one
            _local.connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    return _local.connection


@contextmanager
def _db_cursor():
    """Context manager for database operations with automatic commit.

    Yields:
        sqlite3.Cursor: Database cursor for operations
    """
    conn = _get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()


def init_db() -> None:
    """Initialize the database and create tables if they do not exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with _db_cursor() as c:
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


# ----- Preferences -----
def set_pref(key: str, value: Any) -> None:
    """Set a preference (key, value) in the database.

    Args:
        key: The preference key
        value: The preference value (will be converted to string)
    """
    with _db_cursor() as c:
        c.execute("REPLACE INTO preferences (key, value) VALUES (?, ?)", (key, str(value)))


def get_pref(key: str, default: Any = None) -> Any:
    """Retrieve the value of a preference.

    Args:
        key: The preference key
        default: Default value if key not found

    Returns:
        The preference value if found, otherwise the default value
    """
    with _db_cursor() as c:
        c.execute("SELECT value FROM preferences WHERE key=?", (key,))
        row = c.fetchone()
        return row[0] if row else default


# ----- Extensions -----
def get_extension(ext_id: str) -> Optional[bool]:
    """Retrieve the enabled/disabled state of an extension by its ID.

    Args:
        ext_id: The extension identifier

    Returns:
        True if enabled, False if disabled, None if not found
    """
    with _db_cursor() as c:
        c.execute("SELECT enabled FROM extensions WHERE id=?", (ext_id,))
        row = c.fetchone()
        return row[0] == 1 if row else None


def set_extension_enabled(ext_id: str, enabled: bool) -> None:
    """Enable or disable an extension.

    If the extension does not exist, it will be created.

    Args:
        ext_id: The extension identifier
        enabled: True to enable, False to disable
    """
    with _db_cursor() as c:
        c.execute(
            "INSERT INTO extensions (id, enabled) VALUES (?, ?) "
            "ON CONFLICT(id) DO UPDATE SET enabled=excluded.enabled",
            (ext_id, int(enabled)),
        )


def get_extensions() -> Dict[str, bool]:
    """Return a dictionary with extension ID and enabled/disabled state.

    Returns:
        Dictionary mapping extension IDs to their enabled state
    """
    with _db_cursor() as c:
        c.execute("SELECT id, enabled FROM extensions")
        result = {row[0]: (row[1] == 1) for row in c.fetchall()}
        return result


# ----- API Keys -----
def set_api_key(service: str, key: str) -> None:
    """Save the API key for a service.

    Args:
        service: The service name
        key: The API key
    """
    with _db_cursor() as c:
        c.execute("REPLACE INTO api_keys (service, key) VALUES (?, ?)", (service, key))


def get_api_key(service: str) -> Optional[str]:
    """Retrieve the API key for a service.

    Args:
        service: The service name

    Returns:
        The API key if found, None otherwise
    """
    with _db_cursor() as c:
        c.execute("SELECT key FROM api_keys WHERE service=?", (service,))
        row = c.fetchone()
        return row[0] if row else None
