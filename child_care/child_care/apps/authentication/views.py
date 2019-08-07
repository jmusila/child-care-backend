from .models import User
from .serializers import UserSerializer, RegistrationSerializer
from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class RegistrationAPIView(APIView):
    """ User registration class which allows any user to hit this endpoint
        Authenticated or not authenticated
    """
    parser_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        """ Create new user instance """
        user = request.data.get('user', {})

        try:
            if User.objects.get(email=user['email']):
                message = "a user with that email already exists"
                return Response({"error": message}, status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(username=user['username']):
                message = "a user with that username already exists"
                return Response({"erroe": message}, status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            pass

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
