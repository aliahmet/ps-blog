from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.serializers import UserTokenSerializer


class AuthTokenAPIView(APIView):
    serializer_class = UserTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        Create auth-token
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        # For swagger
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
