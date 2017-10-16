from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from rest_framework_swagger.renderers import OpenAPIRenderer as BaseOpenAPIRenderer
from rest_framework_swagger.settings import swagger_settings


class OpenAPIRenderer(BaseOpenAPIRenderer):
    def get_customizations(self):
        """
        Adds settings, overrides, etc. to the specification.
        """
        return {
            "securityDefinitions": {
                'Bearer': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'Authorization',
                    "description": "Fill value field with Token keyword. ex: **Token ba619b852b9cd53b6bc4a8b451767f07ee4aa631**"
                }
            },
            "security": [
                {"Bearer": []}
            ]

        }


class AllLinksSchemaGenerator(SchemaGenerator):
    """
    All endpoints should be publicly visible.
    """

    def has_view_permissions(self, path, method, view):
        return True


class SwaggerSchemaView(APIView):
    # Let it be accessible by anyone
    _ignore_model_permissions = True
    permission_classes = AllowAny,

    # Don't show yourself
    exclude_from_schema = True

    renderer_classes = [
        OpenAPIRenderer,
    ]

    def get(self, request):
        generator = AllLinksSchemaGenerator(
            title="PS Blog",
        )
        schema = generator.get_schema(request=request)
        return Response(schema)
