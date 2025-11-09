# Launcher Daemon Integration

This document describes the integration between the Launcher UI and the Launcher Daemon for background application indexing and caching.

## Overview

The Launcher application now consists of two components:

1. **Launcher UI** (`cloud.ivanbotty.Launcher`) - The main user interface
2. **Launcher Daemon** (`cloud.ivanbotty.Launcherd`) - Background service for application indexing

The daemon runs in the background, periodically scanning for applications and maintaining a cache. The UI communicates with the daemon via D-Bus to check cache status and receive progress updates.

## Architecture

### D-Bus Interface

The daemon exposes the following D-Bus interface:

**Service Name:** `cloud.ivanbotty.Launcherd`
**Object Path:** `/cloud/ivanbotty/Launcherd`

#### Methods

- `GetCacheStatus() -> (available: bool, cache_path: str, last_updated: int64)`
  - Returns whether the cache is available, its path, and last update timestamp

- `GetIndexingStatus() -> (is_indexing: bool, progress: double, apps_count: int32)`
  - Returns current indexing status, progress (0.0-1.0), and number of apps indexed

- `ForceUpdate()`
  - Triggers an immediate cache update

#### Signals

- `CacheUpdated(apps_count: int32, timestamp: int64)`
  - Emitted when the cache has been updated

- `IndexingProgress(progress: double, apps_count: int32)`
  - Emitted during indexing to report progress

#### Properties

- `Version: string` (read-only)
  - Daemon version number

## Usage

### D-Bus Service Activation

The daemon is configured for automatic D-Bus activation. When the UI tries to connect to the daemon and it's not running, D-Bus will automatically start it.

**D-Bus Service File:** `cloud.ivanbotty.Launcherd.service`
- Installed to: `/usr/share/dbus-1/services/` (system-wide) or `~/.local/share/dbus-1/services/` (user)
- Enables automatic daemon startup on first connection

### Starting the Daemon

The daemon can be started in several ways:

1. **Automatic D-Bus Activation (Recommended)**
   - The daemon starts automatically when the UI first connects
   - No manual intervention needed
   - D-Bus service file handles activation

2. **Automatic Start at Login**
   - The daemon is configured to start automatically at user login via the desktop file
   - Location: `~/.config/autostart/cloud.ivanbotty.Launcherd.desktop`

3. **Manual Start**
   ```bash
   python3 -m cloud.ivanbotty.Launcherd
   ```

4. **Daemon Mode (Background)**
   ```bash
   python3 -m cloud.ivanbotty.Launcherd --daemonize
   ```

5. **Debug Mode**
   ```bash
   python3 -m cloud.ivanbotty.Launcherd --debug
   ```

### UI Behavior

The Launcher UI is designed for instant startup, similar to Spotlight, Krunner, or PowerToys Run:

1. **UI Starts Instantly**
   - On first launch: Scans desktop files (shows progress bar)
   - On subsequent launches: Loads from cache file (instant!)
   - No waiting for daemon connection
   - Cache file checked synchronously (fast file check, no D-Bus calls)

2. **Cache Loading**
   - If cache file exists and is recent (< 1 hour old): Instant load
   - If cache file missing or outdated: Scan desktop files with progress bar
   - **UI creates cache file** after scanning (even without daemon)
   - Daemon (if running) keeps cache fresh in background

3. **Daemon Connection (Background)**
   - Daemon connection happens asynchronously in the background
   - Does not block UI startup
   - If daemon is already running, connection is nearly instant
   - If daemon needs to auto-start, it happens without blocking the UI

4. **Daemon Integration (Optional)**
   - Once daemon connects, it keeps the application cache fresh in the background
   - Future launches benefit from the cached data
   - **Daemon is completely optional** - UI creates and uses cache independently

## Cache Location

The application cache is stored at:
```
~/.cache/cloud.ivanbotty.Launcher/applications_cache.json
```

This cache file is:
- **Created by the UI** after first scan (instant subsequent launches)
- Also maintained by the daemon (if running) during background scanning
- Read by the UI for instant startup on subsequent launches
- Updated automatically every 60 seconds by the daemon (if running)
- Considered stale after 1 hour (triggers rescan)

## Configuration

### Scan Interval

The daemon scans for new applications every 60 seconds by default. This is defined in:
```python
# cloud/ivanbotty/Launcherd/__main__.py
SCAN_INTERVAL = 60  # seconds
```

### Flatpak Permissions

For Flatpak installations, the following permissions are required:

```yaml
finish-args:
  - --own-name=cloud.ivanbotty.Launcherd  # Allow daemon to own D-Bus name
  - --talk-name=org.freedesktop.DBus      # D-Bus communication
```

## Development

### Running Tests

```bash
python3 -m pytest tests/test_daemon_integration.py -v
```

### Checking D-Bus Service Status

```bash
# Check if daemon is running
gdbus introspect --session --dest cloud.ivanbotty.Launcherd --object-path /cloud/ivanbotty/Launcherd

# Monitor D-Bus signals
dbus-monitor --session "type='signal',sender='cloud.ivanbotty.Launcherd'"
```

### Debugging

1. **Check daemon logs**
   ```bash
   python3 -m cloud.ivanbotty.Launcherd --debug
   ```

2. **Check if daemon is registered on D-Bus**
   ```bash
   gdbus call --session --dest org.freedesktop.DBus \
              --object-path /org/freedesktop/DBus \
              --method org.freedesktop.DBus.ListNames | grep Launcherd
   ```

3. **Query cache status**
   ```bash
   gdbus call --session --dest cloud.ivanbotty.Launcherd \
              --object-path /cloud/ivanbotty/Launcherd \
              --method cloud.ivanbotty.Launcherd.GetCacheStatus
   ```

## Troubleshooting

### Daemon Not Starting

1. Check if D-Bus session bus is running
2. Verify desktop file is in autostart directory
3. Check daemon logs for errors

### UI Not Connecting to Daemon

1. Verify daemon is running: `ps aux | grep Launcherd`
2. Check D-Bus service registration (see Debugging section)
3. Check UI logs for connection errors

### Timeout Errors During Daemon Activation

If you see timeout errors like `g-io-error-quark: timeout (24)` when the UI starts:

1. **This is expected behavior** - The daemon is being auto-started via D-Bus and needs time to initialize
2. The UI uses a 30-second timeout for D-Bus method calls to allow the daemon to start
3. If timeouts persist, the daemon may be failing to start - check daemon logs
4. Try starting the daemon manually first: `python3 -m cloud.ivanbotty.Launcherd --debug`

### Cache Not Updating

1. Verify daemon has write permissions to cache directory
2. Check for errors in daemon logs
3. Try forcing an update via D-Bus

## Security Considerations

- The daemon runs with user privileges (not root)
- Cache files are stored in the user's cache directory
- D-Bus communication uses the session bus (not system bus)
- The daemon only reads desktop files from standard locations
- No network access required for core functionality

## Future Improvements

- Add configuration file for scan interval customization
- Implement incremental cache updates (only scan changed directories)
- Add support for watching filesystem changes (inotify)
- Implement cache versioning and migration
- Add metrics and telemetry for cache performance
