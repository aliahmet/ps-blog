from django.utils.deprecation import MiddlewareMixin


class AccessControlAllowMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, PATCH, DELETE'
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, " \
                                                   "Authorization, X-Requested-With, Accept"
        if request.method.lower() == "options":
            response.status_code = 200
        return response
