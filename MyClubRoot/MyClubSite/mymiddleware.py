class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.META['CUSTOM_KEY'] = 'Nige was here'
        
        response = self.get_response(request)

        # assert False
        return response