from gi.repository import Gtk
import cloud.ivanbotty.Launcher.handlers.base_input_handler as bih

class AppHandler(bih.BaseInputHandler):
    def can_handle(self, text):
        # Anything that doesn't fit other handlers and doesn't start with >, ask, or http
        return True

    def handle(self, text, services, listbox):
        apps_service = services.get("app")
        if apps_service:
            apps_service.load_applications()
            apps = apps_service.filter_applications(text)
            listbox.remove_all()
            for app in apps:
                row = Gtk.Label(label=app.name)  # You can replace with Row(app) if you want
                listbox.insert(row, 0)
            if apps:
                apps[0].launch()
