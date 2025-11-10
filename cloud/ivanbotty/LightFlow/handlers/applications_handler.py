import cloud.ivanbotty.LightFlow.handlers.base_input_handler as bih


class AppHandler(bih.BaseInputHandler):
    def can_handle(self, text):
        # Anything that doesn't fit other handlers and doesn't start with >, ask, or http
        return True

    def handle(self, text, services):
        apps_service = services.get("application")
        if apps_service:
            return apps_service.filter_applications(text)
        return None
