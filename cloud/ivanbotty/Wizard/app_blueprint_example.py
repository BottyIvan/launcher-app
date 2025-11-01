"""
Example integration of Blueprint UI with the Wizard module.

This file demonstrates how to use the Blueprint-based UI components
in the existing Wizard application. It can be used as a reference
for migrating the current app.py to use Blueprint UI.
"""

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
from cloud.ivanbotty.Wizard.blueprint_ui import (
    WizardWindowBlueprint,
    WizardPageBlueprint,
    load_wizard_resources
)

# Setup logger
logger = logging.getLogger("WelcomeWizard.Blueprint")
logging.basicConfig(level=logging.INFO)


class WelcomeWizardBlueprint(Adw.Application):
    """
    Welcome Wizard using Blueprint-based UI.
    
    This is an example implementation showing how to integrate
    Blueprint UI components into the existing Wizard application.
    """
    
    def __init__(self, app):
        super().__init__(application_id=app)
        self.win = None  # Main window
        self.carousel = None  # Carousel of contents
        self.wizard_texts = None  # Texts for the wizard
        
        # Load wizard resources
        load_wizard_resources()
        
        try:
            # Load wizard page texts from YAML configuration file
            # Use Path to make this more portable across different working directories
            from pathlib import Path
            wizard_yaml_path = Path(__file__).parent.parent / "Launcher" / "resources" / "wizard.yaml"
            
            if wizard_yaml_path.exists():
                with open(wizard_yaml_path) as f:
                    self.wizard_texts = yaml.safe_load(f)
                logger.info("Wizard texts loaded successfully.")
            else:
                logger.warning(f"Wizard YAML not found at: {wizard_yaml_path}")
                self.wizard_texts = None
        except Exception as e:
            # Log error if loading or parsing fails
            logger.error(f"Error loading wizard texts: {e}")
            self.wizard_texts = None
        
        # Ensure the loaded configuration is a dictionary
        if not isinstance(self.wizard_texts, dict):
            logger.error("Invalid wizard texts structure; expected a dictionary.")
            self.wizard_texts = {}
    
    def on_next(self) -> None:
        """Handles moving to the next page."""
        if not self.carousel:
            return
            
        cur = self.carousel.get_position()
        n = self.carousel.get_n_pages()
        if cur < n - 1:
            next_w = self.carousel.get_nth_page(int(cur) + 1)
            logger.info(f"Scrolling to page {int(cur) + 1}")
            self.carousel.scroll_to(next_w, True)
    
    def on_prev(self) -> None:
        """Handles returning to the previous page."""
        if not self.carousel:
            return
            
        cur = self.carousel.get_position()
        if cur > 0:
            prev_w = self.carousel.get_nth_page(int(cur) - 1)
            self.carousel.scroll_to(prev_w, True)
    
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
        logger.info("Application activated with Blueprint UI")
        
        if self.win is None:
            # Create window using Blueprint
            self.win = WizardWindowBlueprint(application=self)
            self.carousel = self.win.carousel
            
            if self.carousel is None:
                logger.error("Failed to get carousel from Blueprint window")
                return
            
            # Create wizard pages from configuration
            pages_config = self.wizard_texts.get("pages", [])
            
            for i, page_config in enumerate(pages_config):
                title = page_config.get("title", f"Page {i+1}")
                description = page_config.get("description", "Default description.")
                
                # Determine button text and callback
                is_last_page = (i == len(pages_config) - 1)
                button_text = page_config.get(
                    "button_label",
                    "Finish" if is_last_page else "Next"
                )
                callback = self.on_finish if is_last_page else self.on_next
                
                # Create page using Blueprint
                page = WizardPageBlueprint(
                    title=title,
                    subtitle=description,
                    button_text=button_text,
                    callback=callback
                )
                
                self.carousel.append(page)
                logger.info(f"Added page {i+1}: {title}")
        
        self.win.present()
        logger.info("Blueprint-based Wizard window presented")


# Example usage function
def run_blueprint_wizard():
    """
    Run the wizard with Blueprint UI.
    
    This function can be used to test the Blueprint-based wizard
    without modifying the main application entry point.
    """
    import os
    from gi.repository import Gio
    from cloud.ivanbotty.common import find_resource_file
    import cloud.ivanbotty.database.sqlite3 as db
    
    # Load main application resources
    try:
        resource_path = find_resource_file()
        if resource_path:
            resource = Gio.Resource.load(resource_path)
            Gio.resources_register(resource)
    except Exception as e:
        logger.error(f"Failed to load main resources: {e}")
    
    # Initialize database
    try:
        db.init_db()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    # Create and run the application
    app = WelcomeWizardBlueprint(app='cloud.ivanbotty.Wizard.Blueprint')
    app.run()


if __name__ == "__main__":
    run_blueprint_wizard()
