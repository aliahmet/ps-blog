from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers


class SwaggerSchemaView(APIView):
    # Let it be accessible by anyone
    _ignore_model_permissions = True
    permission_classes = AllowAny,

    # Don't show yourself
    exclude_from_schema = True

    # It should serve ui and openapi
    renderer_classes = [
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator(
            title="PS Blog",
            description="Some endpoints require authetnication. Please authenticate in order to see all endpoints",
        )
        schema = generator.get_schema(request=request)
        return Response(schema)
