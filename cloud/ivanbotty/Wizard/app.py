"""Welcome Wizard application for first-time setup.

This module provides a welcome wizard that guides users through the initial
setup process when they first launch the application.
"""
import logging
import subprocess
import sys
import threading
from typing import Optional

import gi
import yaml

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk

from cloud.ivanbotty.Launcher.widget.window import Window
from cloud.ivanbotty.Wizard.components.page import Page
from cloud.ivanbotty.common import find_extensions_yaml

logger = logging.getLogger(__name__)


class WelcomeWizard(Adw.Application):
    """Welcome Wizard application for first-time user onboarding.

    Attributes:
        win: Main application window
        content: Carousel widget containing wizard pages
        wizard_texts: Configuration dictionary loaded from wizard.yaml
    """

    def __init__(self, app: str) -> None:
        """Initialize the Welcome Wizard application.

        Args:
            app: Application ID string
        """
        super().__init__(application_id=app)
        self.win: Optional[Window] = None
        self.content: Optional[Adw.Carousel] = None
        self.wizard_texts: dict = {}

        try:
            # Load wizard page texts from YAML configuration file
            yaml_path = find_extensions_yaml("wizard.yaml")
            with open(yaml_path) as f:
                self.wizard_texts = yaml.safe_load(f)
            logger.info("Wizard texts loaded successfully")
        except Exception as e:
            logger.error(f"Error loading wizard texts: {e}")
            self.wizard_texts = {}

        # Ensure the loaded configuration is a dictionary
        if not isinstance(self.wizard_texts, dict):
            logger.error("Invalid wizard texts structure; expected a dictionary")
            self.wizard_texts = {}

    def on_next(self) -> None:
        """Handle moving to the next page in the wizard."""
        if self.content is None:
            return

        cur = self.content.get_position()
        n = self.content.get_n_pages()
        if cur < n - 1:
            next_w = self.content.get_nth_page(cur + 1)
            logger.info(f"Scrolling to page {cur + 1}")
            self.content.scroll_to(next_w, True)

    def on_prev(self) -> None:
        """Handle returning to the previous page in the wizard."""
        if self.content is None:
            return

        cur = self.content.get_position()
        if cur > 0:
            prev_w = self.content.get_nth_page(cur - 1)
            self.content.scroll_to(prev_w)

    def on_finish(self) -> None:
        """Handle completion of the wizard and launch main application."""
        logger.info("Wizard completed! Launching main app...")

        # Mark onboarding as complete
        from cloud.ivanbotty.Launcher.config.config import mark_onboarding_complete
        mark_onboarding_complete()

        threading.Thread(
            target=lambda: subprocess.run([sys.executable, "-m", "cloud.ivanbotty.Launcher"]),
            daemon=True,
        ).start()

        if self.win:
            self.win.close()
            logger.info("Welcome wizard application closed")

    def do_activate(self) -> None:
        """Activate the application and show the window."""
        logger.info("Application activated")
        if self.win is None:
            self.win = Window(application=self)

            # Main box with padding
            main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
            main_box.set_margin_top(12)
            main_box.set_margin_bottom(12)

            # Carousel with smooth transitions
            self.content = Adw.Carousel()
            self.content.set_allow_mouse_drag(True)
            self.content.set_allow_scroll_wheel(True)
            
            # Add carousel indicators with dots style
            indicator = Adw.CarouselIndicatorDots(carousel=self.content)
            indicator.set_halign(Gtk.Align.CENTER)
            
            main_box.append(self.content)
            main_box.append(indicator)
            self.win.set_content(main_box)

            # Build wizard pages from configuration
            pages_config = self.wizard_texts.get("pages", [])
            pages = [
                Page.make_page(
                    title=text.get("title", f"Page {i + 1}"),
                    subtitle=text.get("description", "Default description."),
                    button_text=text.get(
                        "button_label", "Next" if i < len(pages_config) - 1 else "Finish"
                    ),
                    callback=self.on_next if i < len(pages_config) - 1 else self.on_finish,
                    icon_name=text.get("icon", None),
                )
                for i, text in enumerate(pages_config)
            ]

            for page in pages:
                self.content.append(page)

        self.win.present()
