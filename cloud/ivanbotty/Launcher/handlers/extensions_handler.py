import cloud.ivanbotty.Launcher.handlers.base_input_handler as bih

class ExtensionHandler(bih.BaseInputHandler):
    def can_handle(self, text):
        # Anything that doesn't fit other handlers and doesn't start with >, ask, or http
        return True

    def handle(self, text, services):
        extensions_service = services.get("extensions")
        if extensions_service:
            return extensions_service.list_extensions()
        return None
