#!/usr/bin/env python3
from concurrent.futures import thread
import logging
import yaml
import gi
import subprocess
import sys
import threading

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk

from cloud.ivanbotty.Launcher.widget.window import Window
from cloud.ivanbotty.Wizard.components.page import Page

# Setup logger
logger = logging.getLogger("WelcomeWizard")
logging.basicConfig(level=logging.INFO)

class WelcomeWizard(Adw.Application):
    def __init__(self, app):
        super().__init__(application_id=app)
        self.win = None  # Main window
        self.content = None  # Carousel of contents
        self.wizard_texts = None  # Texts for the wizard

        try:
            # Load wizard page texts from YAML configuration file
            with open("./cloud/ivanbotty/Launcher/resources/wizard.yaml") as f:
                self.wizard_texts = yaml.safe_load(f)
            logger.info("Wizard texts loaded successfully.")
        except Exception as e:
            # Log error if loading or parsing fails
            logger.error(f"Error loading wizard texts: {e}")
            self.wizard_texts = None

        # Ensure the loaded configuration is a dictionary
        if not isinstance(self.wizard_texts, dict):
            logger.error("Invalid wizard texts structure; expected a dictionary.")
            self.wizard_texts = []

    def on_next(self) -> None:
        """Handles moving to the next page."""
        cur = self.content.get_position()
        n = self.content.get_n_pages()
        if cur < n - 1:
            next_w = self.content.get_nth_page(cur + 1)
            logger.info(f"Scrolling to page {cur + 1}")
            self.content.scroll_to(next_w, True)

    def on_prev(self) -> None:
        """Handles returning to the previous page."""
        cur = self.content.get_position()
        if cur > 0:
            prev_w = self.content.get_nth_page(cur - 1)
            self.content.scroll_to(prev_w)

    def on_finish(self) -> None:
        """Handles the end of the wizard."""
        logger.info("Wizard completed! Launching main app...")

        threading.Thread(
            target=lambda: subprocess.run([sys.executable, "-m", "cloud.ivanbotty.Launcher"]),
            daemon=True
        ).start()

        if self.win:
            self.win.close()
            logger.info("Welcome wizard application closed.")

    def do_activate(self) -> None:
        """Activates the application and shows the window."""
        logger.info("Application activated")
        if self.win is None:
            self.win = Window(application=self)

            # Main box with padding
            main_box = Gtk.Box(orientation="vertical", spacing=24)

            # Carousel and indicators
            self.content = Adw.Carousel()
            indicator = Adw.CarouselIndicatorDots(carousel=self.content)
            main_box.append(self.content)
            main_box.append(indicator)
            self.win.set_content(main_box)

            # Wizard pages
            pages = [
                Page.make_page(
                    title=text.get("title", f"Page {i+1}"),
                    subtitle=text.get("description", "Default description."),
                    button_text=text.get("button_label", "Next" if i < len(self.wizard_texts.get("pages", [])) - 1 else "Finish"),
                    callback=self.on_next if i < len(self.wizard_texts.get("pages", [])) - 1 else self.on_finish
                )
                for i, text in enumerate(self.wizard_texts.get("pages", []))
            ]

            for page in pages:
                self.content.append(page)

        self.win.present()