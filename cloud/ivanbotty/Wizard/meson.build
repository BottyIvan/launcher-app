# Install cloud.ivanbotty.Wizard package
wizard_sources = [
  '__init__.py',
  '__main__.py',
  'app.py',
]

python.install_sources(
  wizard_sources,
  subdir: 'cloud/ivanbotty/Wizard',
  pure: true,
)

# Install components submodule
python.install_sources(
  'components/__init__.py',
  'components/page.py',
  subdir: 'cloud/ivanbotty/Wizard/components',
  pure: true,
)
