import gi
gi.require_version("Adw", "1")
from gi.repository import Adw
import cloud.ivanbotty.database.sqlite3 as db

class Preferences(Adw.PreferencesDialog):
    def __init__(self, app):
        super().__init__(title="Preferences")
        self.app = app

        # Create the main preferences page
        page = Adw.PreferencesPage()

        # General settings group
        general_group = Adw.PreferencesGroup(title="General")

        # Switch row for enabling/disabling compact layout
        self.switch = Adw.SwitchRow(
            active=(db.get_pref("layout", "default") == "compact"),
            title="Use compact layout",
            subtitle="Switch between compact and default layout."
        )
        # Save layout preference when toggled
        self.switch.connect("notify::active", 
            lambda sw, _: db.set_pref("layout", "compact" if sw.get_active() else "default"))
        general_group.add(self.switch)

        # Extensions settings group
        extension_group = Adw.PreferencesGroup(title="Extensions")

        # Get available extensions and their saved states
        extension_list = self.app.extensions_service.list_extensions()
        saved_exts = db.get_extensions()

        # Add a switch for each extension to enable/disable it
        for extension in extension_list:
            self.switch = Adw.SwitchRow(
                active=saved_exts.get(extension.name, extension.enabled),
                title=extension.name or "Unnamed Extension",
                subtitle=extension.description or "No description available."
            )
            # Save extension enabled state when toggled
            self.switch.connect("notify::active",
                lambda sw, _, ext_id=extension.service: db.set_extension_enabled(ext_id, sw.get_active()))
            extension_group.add(self.switch)

        # API keys settings group
        api_group = Adw.PreferencesGroup(title="API Keys")

        # Row for Gemini API key input
        gemini_row = Adw.PasswordEntryRow(
            title="Gemini API Key",
            text=db.get_api_key("gemini") or ""
        )
        gemini_row.set_show_apply_button(True)
        # Save API key when "Apply" is pressed
        gemini_row.connect("apply", self.on_api_key_apply, "gemini")

        api_group.add(gemini_row)

        # About group for application info
        about_group = Adw.PreferencesGroup(title="About")

        # Information row with app details
        info_row = Adw.ActionRow(
            title="About",
            subtitle="Information about this application."
        )
        info_row.set_activatable(True)
        # Show about dialog when activated
        def on_info_row_activated(row):
            about = Adw.AboutDialog.new_from_appdata("/cloud/ivanbotty/Launcher/resources/appdata.xml", "0.0.1")
            about.set_developers(["Ivan Bottigelli https://ivanbotty.cloud"])
            about.set_copyright("© 2025 Ivan Bottigelli.")
            about.present()

        info_row.connect("activated", on_info_row_activated)

        about_group.add(info_row)

        # Add all groups to the page and the page to the dialog
        page.add(general_group)
        page.add(extension_group)
        page.add(api_group)
        page.add(about_group)
        self.add(page)

    def on_api_key_apply(self, row, service):
        # Save the API key if not empty
        text = row.get_text().strip()
        if text:
            db.set_api_key(service, text)