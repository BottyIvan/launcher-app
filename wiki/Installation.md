# Installation Guide

This guide covers installation methods for Launcher on Linux systems.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Flatpak Installation (Recommended)](#flatpak-installation-recommended)
- [Installing from Source](#installing-from-source)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Verification](#verification)
- [Updating](#updating)
- [Uninstallation](#uninstallation)

## Prerequisites

### System Requirements

- **Operating System**: Linux (tested on GNOME-based distributions)
- **Python**: 3.11 or higher
- **GTK**: GTK4 libraries
- **Display Server**: Wayland or X11

### Required Dependencies

The following dependencies are automatically included when using Flatpak:
- PyGObject >= 3.44
- GTK4 and Adwaita libraries
- Python standard library (sqlite3)
- google-generativeai >= 0.3.0 (for AI features)

## Flatpak Installation (Recommended)

Flatpak is the recommended installation method as it provides a sandboxed environment with all dependencies included.

### Step 1: Install Flatpak

If you don't have Flatpak installed, install it first:

**On Ubuntu/Debian:**
```bash
sudo apt install flatpak
```

**On Fedora:**
```bash
sudo dnf install flatpak
```

**On Arch Linux:**
```bash
sudo pacman -S flatpak
```

### Step 2: Add Flathub Repository (Optional)

```bash
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

### Step 3: Build and Install Launcher

```bash
# Clone the repository
git clone https://github.com/BottyIvan/launcher-app.git
cd launcher-app

# Build and install with Flatpak
flatpak-builder --user --install --force-clean build-dir manifest.yaml
```

### Step 4: Launch the Application

```bash
flatpak run cloud.ivanbotty.Launcher
```

## Installing from Source

For development or if you prefer to run without Flatpak:

### Step 1: Install System Dependencies

**On Ubuntu/Debian:**
```bash
sudo apt install python3 python3-pip python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adwaita-1
```

**On Fedora:**
```bash
sudo dnf install python3 python3-pip python3-gobject gtk4 libadwaita
```

**On Arch Linux:**
```bash
sudo pacman -S python python-pip python-gobject gtk4 libadwaita
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/BottyIvan/launcher-app.git
cd launcher-app
```

### Step 3: Install Python Dependencies

```bash
pip3 install --user PyGObject google-generativeai
```

### Step 4: Run the Application

```bash
# Run the main launcher
python3 -m cloud.ivanbotty.Launcher

# Or run the welcome wizard
python3 -m cloud.ivanbotty.Wizard
```

### Step 5: Optional - Install with Meson

```bash
# Configure the build
meson setup builddir

# Compile and install
meson compile -C builddir
sudo meson install -C builddir
```

## Platform-Specific Instructions

### GNOME Desktop

Launcher integrates seamlessly with GNOME. After installation, you can:
- Launch from Activities
- Pin to favorites
- Use keyboard shortcuts

### KDE Plasma

Launcher works on KDE but may have a different visual style:
1. Install as described above
2. Add to application menu
3. Configure keyboard shortcuts in System Settings

### Other Desktop Environments

Launcher should work on any modern Linux desktop environment with GTK4 support. Ensure your system has:
- GTK4 runtime
- Wayland or X11 display server
- D-Bus support

## Verification

After installation, verify that Launcher is working:

```bash
# For Flatpak installation
flatpak run cloud.ivanbotty.Launcher

# For source installation
python3 -m cloud.ivanbotty.Launcher
```

You should see the Launcher window appear.

## Updating

### Flatpak Installation

```bash
# Rebuild and reinstall
cd launcher-app
git pull
flatpak-builder --user --install --force-clean build-dir manifest.yaml
```

### Source Installation

```bash
cd launcher-app
git pull

# If using Meson
meson compile -C builddir
sudo meson install -C builddir
```

## Uninstallation

### Flatpak Installation

```bash
flatpak uninstall cloud.ivanbotty.Launcher
```

### Meson Installation

```bash
cd launcher-app/builddir
sudo ninja uninstall
```

### Manual Cleanup

Remove user data and configurations:
```bash
rm -rf ~/.var/app/cloud.ivanbotty.Launcher  # Flatpak data
rm -rf ~/.local/share/cloud.ivanbotty.Launcher  # Local data
```

## Troubleshooting Installation

### Common Issues

**Issue: "GTK4 not found"**
- Solution: Install GTK4 development libraries for your distribution

**Issue: "PyGObject import error"**
- Solution: Install python3-gi package for your distribution

**Issue: "Flatpak build fails"**
- Solution: Ensure you have the latest flatpak-builder and dependencies

**Issue: "Permission denied"**
- Solution: Check that you have write permissions or use `sudo` where appropriate

For more troubleshooting help, see [FAQ](FAQ.md).

## Next Steps

After installation:
1. Read the [Usage Guide](Usage-Guide.md) to learn how to use Launcher
2. Explore [Features](Features.md) to discover what Launcher can do
3. Check [Configuration](Configuration.md) to customize your experience
