project('lightflow-app',
  version: '0.0.1',
  meson_version: '>= 0.59.0',
  default_options: [
    'warning_level=2',
  ],
)

# Get Python installation
python = import('python').find_installation('python3')

# Prefix and data directories
prefix = get_option('prefix')
bindir = prefix / get_option('bindir')
datadir = prefix / get_option('datadir')
pkgdatadir = datadir / meson.project_name()

# Process Python package structure
subdir('cloud')

# Install desktop file
install_data(
  'cloud.ivanbotty.LightFlow.desktop',
  install_dir: datadir / 'applications',
)

# Install daemon desktop file for autostart
install_data(
  'cloud.ivanbotty.LightFlowD.desktop',
  install_dir: datadir / 'applications',
)

# Install daemon autostart file
install_data(
  'cloud.ivanbotty.LightFlowD.desktop',
  install_dir: get_option('sysconfdir') / 'xdg/autostart',
)

# Install SVG icon
install_data(
  'cloud/ivanbotty/LightFlow/resources/cloud.ivanbotty.LightFlow.svg',
  install_dir: datadir / 'icons/hicolor/scalable/apps',
)

# Install manifest.yaml
install_data(
  'manifest.yaml',
  install_dir: pkgdatadir,
)

# Install resources (icons, data files)
install_subdir(
  'cloud/ivanbotty/LightFlow/resources',
  install_dir: pkgdatadir / 'LightFlow',
  strip_directory: false,
)

# Compile the gresource file
gresource_xml = 'cloud/ivanbotty/LightFlow/resources/resources.xml'
gresource_target = custom_target(
  'resources.gresource',
  input: gresource_xml,
  output: 'resources.gresource',
  command: ['glib-compile-resources', '@INPUT@', '--target=@OUTPUT@', '--sourcedir=' + meson.project_source_root() / 'cloud/ivanbotty/LightFlow/resources'],
  install: true,
  install_dir: pkgdatadir / 'LightFlow/resources',
)

# Create wrapper script for the launcher
configure_file(
  input: 'lightflow-wrapper.sh.in',
  output: 'cloud-ivanbotty-lightflow',
  configuration: {
    'PYTHON': python.full_path(),
  },
  install: true,
  install_dir: bindir,
  install_mode: 'rwxr-xr-x',
)

# Create wrapper script for the daemon
configure_file(
  input: 'lightflowd-wrapper.sh.in',
  output: 'cloud-ivanbotty-lightflowd',
  configuration: {
    'PYTHON': python.full_path(),
  },
  install: true,
  install_dir: bindir,
  install_mode: 'rwxr-xr-x',
)

# Install D-Bus service file for daemon auto-activation
configure_file(
  input: 'cloud.ivanbotty.LightFlowD.service.in',
  output: 'cloud.ivanbotty.LightFlowD.service',
  configuration: {
    'BINDIR': bindir,
  },
  install: true,
  install_dir: datadir / 'dbus-1/services',
)

# Summary
summary({
  'prefix': prefix,
  'bindir': bindir,
  'datadir': datadir,
  'pkgdatadir': pkgdatadir,
}, section: 'Directories')

summary({
  'Python': python.full_path(),
}, section: 'Programs')
