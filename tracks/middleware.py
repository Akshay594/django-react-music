class StackOverFlowMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.translations = {
            "en": {"greeting": "Hello", "header": "Welcome Django!"},
            "nl": {"greeting": "Hallo", "header": "Welkom Django!"},
        }

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        if "nl" in request.META['HTTP_ACCEPT_LANGUAGE']:
            request.context_data["translations"] = self.translations
            return response
        return response
