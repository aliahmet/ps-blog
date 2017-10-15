from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers


class AllLinksSchemaGenerator(SchemaGenerator):
    def has_view_permissions(self, path, method, view):
        return True


class SwaggerSchemaView(APIView):
    # Let it be accessible by anyone
    _ignore_model_permissions = True
    permission_classes = AllowAny,

    # Don't show yourself
    exclude_from_schema = True

    renderer_classes = [
        renderers.OpenAPIRenderer,
    ]

    def get(self, request):
        generator = AllLinksSchemaGenerator(
            title="PS Blog",
        )
        schema = generator.get_schema(request=request)
        return Response(schema)
