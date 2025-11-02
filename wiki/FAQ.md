# FAQ and Troubleshooting

Frequently asked questions and solutions to common issues.

## Table of Contents

- [General Questions](#general-questions)
- [Installation Issues](#installation-issues)
- [Usage Questions](#usage-questions)
- [Performance Issues](#performance-issues)
- [Configuration Problems](#configuration-problems)
- [Extension Issues](#extension-issues)
- [Development Questions](#development-questions)
- [Platform-Specific Issues](#platform-specific-issues)

## General Questions

### What is Launcher?

Launcher is a modern desktop application launcher for Linux built with GTK4 and Adwaita. It provides instant search capabilities for installed applications, a built-in calculator, and an extensible architecture for adding custom functionality.

### What platforms does Launcher support?

Launcher is designed for Linux desktop environments. It works best on:
- GNOME (primary target)
- KDE Plasma
- XFCE
- Other GTK4-compatible desktop environments

### Is Launcher free and open source?

Yes! Launcher is licensed under GPL-3.0-or-later and is completely free and open source.

### How is Launcher different from GNOME's built-in search?

- **Standalone**: Launcher is a separate application
- **Faster startup**: Optimized for quick launches
- **More customizable**: Extension system and preferences
- **Calculator built-in**: No need to switch apps
- **Portable**: Works across different desktop environments

### How much memory does Launcher use?

Launcher typically uses 30-50MB of RAM when running, with minimal CPU usage during idle. Memory usage may increase temporarily during application discovery and caching.

## Installation Issues

### "GTK4 not found" error

**Problem**: Missing GTK4 libraries

**Solution**:
```bash
# Ubuntu/Debian
sudo apt install libgtk-4-1 gir1.2-gtk-4.0

# Fedora
sudo dnf install gtk4

# Arch Linux
sudo pacman -S gtk4
```

### "PyGObject import error"

**Problem**: Python GTK bindings not installed

**Solution**:
```bash
# Ubuntu/Debian
sudo apt install python3-gi python3-gi-cairo

# Fedora
sudo dnf install python3-gobject

# Arch Linux
sudo pacman -S python-gobject

# Or via pip (not recommended)
pip3 install PyGObject
```

### Flatpak build fails

**Problem**: Missing flatpak-builder or dependencies

**Solution**:
```bash
# Install flatpak-builder
sudo apt install flatpak-builder  # Ubuntu/Debian
sudo dnf install flatpak-builder  # Fedora
sudo pacman -S flatpak-builder    # Arch

# Ensure you have GNOME runtime
flatpak install flathub org.gnome.Platform//48 org.gnome.Sdk//48

# Clean and rebuild
rm -rf build-dir .flatpak-builder
flatpak-builder --user --install --force-clean build-dir manifest.yaml
```

### "Permission denied" when installing

**Problem**: Insufficient permissions

**Solution**:
- Use `--user` flag for user-level install
- Or use `sudo` for system-wide install
- Check file permissions in the repository directory

### Application doesn't start after installation

**Problem**: Missing dependencies or configuration

**Solution**:
```bash
# For Flatpak, check if installed
flatpak list | grep Launcher

# Try running with verbose output
flatpak run -v cloud.ivanbotty.Launcher

# Check logs
journalctl --user -f | grep launcher

# For source install, check Python path
python3 -c "import gi; gi.require_version('Gtk', '4.0'); from gi.repository import Gtk"
```

## Usage Questions

### How do I open Launcher?

**Methods**:
1. **From application menu**: Search for "Launcher"
2. **Command line**: `flatpak run cloud.ivanbotty.Launcher`
3. **Keyboard shortcut**: Configure in system settings (e.g., Super+Space)

### Applications are not showing up

**Problem**: Desktop files not found or cached

**Solution**:
1. Check if applications have `.desktop` files
2. Verify desktop file locations:
   ```bash
   ls /usr/share/applications
   ls ~/.local/share/applications
   ```
3. Clear cache and restart:
   ```bash
   rm -rf ~/.local/share/cloud.ivanbotty.Launcher/cache
   ```
4. For Flatpak apps, ensure they're visible:
   ```bash
   ls ~/.local/share/flatpak/exports/share/applications
   ```

### Icons are missing or incorrect

**Problem**: Icon theme or cache issues

**Solution**:
1. Install a complete icon theme:
   ```bash
   sudo apt install adwaita-icon-theme
   ```
2. Update icon cache:
   ```bash
   gtk-update-icon-cache
   ```
3. Check GTK settings:
   ```bash
   gsettings get org.gnome.desktop.interface icon-theme
   ```

### Search is not finding apps I know are installed

**Problem**: Search algorithm or desktop file issues

**Solution**:
1. Try exact name of the application
2. Check if app has NoDisplay=true in desktop file
3. Verify desktop file format
4. Enable "show hidden apps" in preferences
5. Check application categories and keywords

### How do I use the calculator?

**Usage**: Just type mathematical expressions directly:

```
Type: 2 + 2
Result: 4

Type: sqrt(16)
Result: 4.0

Type: sin(pi/2)
Result: 1.0
```

**Supported operations**:
- Basic: `+`, `-`, `*`, `/`, `**` (power), `%` (modulo)
- Functions: `sqrt`, `sin`, `cos`, `tan`, `log`, `abs`, `ceil`, `floor`
- Constants: `pi`, `e`

### How do I switch between compact and extended view?

**Methods**:
1. Press `Tab` key
2. Click view toggle button (if available)
3. Preference is saved automatically

## Performance Issues

### Launcher is slow to start

**Possible causes and solutions**:

1. **First launch**: Cache is being built
   - Solution: Wait for initial scan to complete
   - Subsequent launches will be faster

2. **Large number of applications**:
   - Solution: Increase cache size in preferences
   - Consider disabling unused Flatpak remotes

3. **Slow disk I/O**:
   - Solution: Use SSD if possible
   - Check disk health

4. **Debug mode enabled**:
   - Solution: Disable debug logging
   ```bash
   unset LAUNCHER_DEBUG
   unset LAUNCHER_LOG_LEVEL
   ```

### Search results appear slowly

**Problem**: Database queries or search algorithm

**Solution**:
1. Ensure instant search is enabled in preferences
2. Reduce max results limit
3. Disable "search in descriptions" for faster search
4. Clear and rebuild cache

### High memory usage

**Problem**: Memory leak or large cache

**Solution**:
1. Restart Launcher periodically
2. Check cache size settings
3. Disable unused extensions
4. Report persistent memory issues on GitHub

### Application hangs or freezes

**Problem**: Thread deadlock or UI blocking

**Solution**:
1. Check system logs for errors
2. Try disabling extensions one by one
3. Run with debug logging:
   ```bash
   LAUNCHER_LOG_LEVEL=DEBUG flatpak run cloud.ivanbotty.Launcher
   ```
4. Report issue with logs

## Configuration Problems

### Preferences not saving

**Problem**: Database write permissions or corruption

**Solution**:
```bash
# Check database location
ls -la ~/.local/share/cloud.ivanbotty.Launcher/

# For Flatpak
ls -la ~/.var/app/cloud.ivanbotty.Launcher/data/

# Check permissions
chmod 644 ~/.local/share/cloud.ivanbotty.Launcher/launcher.db

# If corrupted, backup and reset
mv launcher.db launcher.db.bak
# Restart Launcher to create new database
```

### Settings reset after each launch

**Problem**: Database not persisting or Flatpak permissions

**Solution**:
```bash
# For Flatpak, ensure data directory is writable
flatpak override --user --filesystem=xdg-data/cloud.ivanbotty.Launcher cloud.ivanbotty.Launcher

# Check if database is in read-only location
```

### Custom keyboard shortcuts not working

**Problem**: System-wide shortcuts or conflict

**Solution**:
1. Use system settings to set global shortcut
2. Ensure no conflicts with existing shortcuts
3. Check desktop environment documentation:
   - GNOME: Settings → Keyboard → Custom Shortcuts
   - KDE: System Settings → Shortcuts

## Extension Issues

### Extension won't enable

**Problem**: Missing dependencies or configuration

**Solution**:
1. Check extension requirements
2. For AI extension, set API key:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```
3. Check extension YAML syntax
4. View logs for error messages

### AI Assistant not responding

**Problem**: API key, network, or API issues

**Solution**:
1. Verify API key is set:
   ```bash
   echo $GEMINI_API_KEY
   ```
2. Check network connectivity
3. Verify API quota/limits
4. Check API endpoint is accessible

### Math calculator giving wrong results

**Problem**: Expression parsing or operator precedence

**Solution**:
1. Use parentheses for complex expressions
2. Check function names (e.g., `sqrt` not `square_root`)
3. Verify angle mode (radians vs degrees)
4. Report calculation bugs on GitHub

### Extension conflicts

**Problem**: Multiple extensions handling same input

**Solution**:
1. Check extension priorities
2. Disable conflicting extensions
3. Reorder extensions in configuration

## Development Questions

### How do I set up a development environment?

See the detailed [Contributing Guide](Contributing.md#development-setup).

**Quick setup**:
```bash
git clone https://github.com/BottyIvan/launcher-app.git
cd launcher-app
pip3 install --user PyGObject google-generativeai black flake8 mypy
python3 -m cloud.ivanbotty.Launcher
```

### Tests are failing

**Problem**: Missing dependencies or test environment issues

**Solution**:
```bash
# Install test dependencies
pip3 install --user PyGObject

# Run tests with verbose output
python3 -m unittest discover tests/ -v

# Check specific failing test
python3 -m unittest tests.test_utils.TestAppInitUtils -v

# Some tests may be skipped if GTK4 is not available in test environment
```

### How do I create a new extension?

See [Architecture](Architecture.md) and [API Reference](API-Reference.md).

**Basic steps**:
1. Create handler class extending `BaseInputHandler`
2. Create service class with business logic
3. Add extension definition to `extensions.yaml`
4. Test and submit PR

### Type checking errors with MyPy

**Problem**: Type hints or stub files

**Solution**:
```bash
# Install type stubs
pip3 install types-PyYAML

# Run MyPy with relaxed settings for GTK
mypy --ignore-missing-imports cloud/ivanbotty
```

## Platform-Specific Issues

### GNOME

**Wayland issues**:
```bash
# Force X11 if Wayland has issues
GDK_BACKEND=x11 flatpak run cloud.ivanbotty.Launcher
```

**HiDPI scaling**:
```bash
# Adjust scaling
GDK_SCALE=2 flatpak run cloud.ivanbotty.Launcher
```

### KDE Plasma

**Theme inconsistencies**:
- Install Breeze-GTK theme for better integration
- Or set GTK theme to Adwaita

**Qt/GTK mixing**:
- Visual style may differ from Qt apps
- This is expected behavior

### XFCE

**Compositor issues**:
- Enable compositor for smooth animations
- Settings → Window Manager Tweaks → Compositor

### Tiling Window Managers (i3, Sway)

**Floating window**:
```bash
# For i3 config
for_window [app_id="cloud.ivanbotty.Launcher"] floating enable

# For Sway
for_window [app_id="cloud.ivanbotty.Launcher"] floating enable, sticky enable
```

## Getting More Help

### Check Logs

**System logs**:
```bash
# For systemd
journalctl --user -f | grep launcher

# Application logs (if enabled)
tail -f ~/.local/share/cloud.ivanbotty.Launcher/launcher.log
```

**Debug mode**:
```bash
LAUNCHER_LOG_LEVEL=DEBUG flatpak run cloud.ivanbotty.Launcher 2>&1 | tee launcher-debug.log
```

### Report an Issue

If your problem isn't covered here:

1. **Search existing issues**: https://github.com/BottyIvan/launcher-app/issues
2. **Gather information**:
   - Operating system and version
   - Desktop environment
   - Launcher version
   - Steps to reproduce
   - Error messages or logs
3. **Create new issue**: Provide all gathered information
4. **Be patient**: Maintainers will respond when available

### Community Support

- **GitHub Issues**: https://github.com/BottyIvan/launcher-app/issues
- **Email**: droidbotty@gmail.com

## Quick Troubleshooting Checklist

When something goes wrong, try these steps:

1. ☐ Restart Launcher
2. ☐ Check system updates
3. ☐ Clear cache and restart
4. ☐ Check logs for errors
5. ☐ Try with default configuration
6. ☐ Verify dependencies are installed
7. ☐ Check GitHub issues for similar problems
8. ☐ Enable debug logging
9. ☐ Report issue with detailed information

## Additional Resources

- [Installation Guide](Installation.md)
- [Usage Guide](Usage-Guide.md)
- [Configuration](Configuration.md)
- [Architecture](Architecture.md)
- [Contributing](Contributing.md)
