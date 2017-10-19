from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.permissions import IsOwnerOrReadOnly, IsSelfOrReadOnly
from blog.serializers import UserTokenSerializer, UserRegisterSerializer, UserSerializer


class LoginAPIView(APIView):
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


class RegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        Create a new user
        """
        self.create(request, *args, **kwargs)
        token, created = Token.objects.get_or_create(user=self.user)
        return Response({'token': token.key})

    def perform_create(self, serializer):
        self.user = serializer.save()


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = IsSelfOrReadOnly,
    lookup_url_kwarg = "pk"

    def get_object(self):
        return self.request.user

    def get(self, request, pk):
        """
        Retrieve current users details
        """
        return self.retrieve(request, pk)

    def put(self, request, pk):
        """
        Update current users details
        """
        return self.update(request, pk)

    def patch(self, request, pk):
        """
        Update current users details partially
        """
        return self.partial_update(request, pk)
