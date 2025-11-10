# Install cloud.ivanbotty.LightFlow package
lightflow_sources = [
  '__init__.py',
  '__main__.py',
  'app.py',
]

python.install_sources(
  lightflow_sources,
  subdir: 'cloud/ivanbotty/LightFlow',
  pure: true,
)

# Install config submodule
python.install_sources(
  'config/__init__.py',
  'config/config.py',
  subdir: 'cloud/ivanbotty/LightFlow/config',
  pure: true,
)

# Install controller submodule
python.install_sources(
  'controller/__init__.py',
  'controller/event_base_controller.py',
  'controller/event_click_controller.py',
  'controller/event_key_controller.py',
  'controller/event_search_controller.py',
  subdir: 'cloud/ivanbotty/LightFlow/controller',
  pure: true,
)

# Install handlers submodule
python.install_sources(
  'handlers/__init__.py',
  'handlers/ai_handler.py',
  'handlers/applications_handler.py',
  'handlers/base_input_handler.py',
  'handlers/command_handler.py',
  'handlers/extensions_handler.py',
  'handlers/link_handler.py',
  'handlers/math_handler.py',
  subdir: 'cloud/ivanbotty/LightFlow/handlers',
  pure: true,
)

# Install helper submodule
python.install_sources(
  'helper/__init__.py',
  'helper/load_class_instance.py',
  'helper/parser.py',
  'helper/portal_launcher.py',
  'helper/thread_manager.py',
  subdir: 'cloud/ivanbotty/LightFlow/helper',
  pure: true,
)

# Install models submodule
python.install_sources(
  'models/__init__.py',
  'models/applications_model.py',
  'models/extension_model.py',
  subdir: 'cloud/ivanbotty/LightFlow/models',
  pure: true,
)

# Install services submodule
python.install_sources(
  'services/__init__.py',
  'services/ai_service.py',
  'services/applications_service.py',
  'services/command_service.py',
  'services/daemon_client.py',
  'services/extensions_service.py',
  'services/math_service.py',
  subdir: 'cloud/ivanbotty/LightFlow/services',
  pure: true,
)

# Install widget submodule
python.install_sources(
  'widget/__init__.py',
  'widget/footer.py',
  'widget/preferences.py',
  'widget/progress_bar.py',
  'widget/row.py',
  'widget/search_entry.py',
  'widget/window.py',
  subdir: 'cloud/ivanbotty/LightFlow/widget',
  pure: true,
)
