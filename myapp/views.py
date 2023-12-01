from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.authtoken.serializers import AuthTokenSerializer

from django.contrib.auth import login

# Token Authentication
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication

from .models import get_or_none, Technology
from .serializers import UserSerializer, RegisterSerializer, VerifyUserSerializer, TechnologySerializer

from django.contrib.auth.models import User

from django.core.files.base import ContentFile
from rest_framework.parsers import FileUploadParser


class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class UserVerify(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = VerifyUserSerializer(data=request.query_params)
        import pdb;pdb.set_trace()
        serializer.is_valid(raise_exception=True)
        user = get_or_none(User, **serializer.validated_data)
        if user:
            return Response({'msg': 'success'}, status=200)

        return Response({'msg': 'No user associated with this email or username!'}, status=200)


class TechnologyView(APIView):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def get(self, request):
        qs = Technology.objects.all()
        return Response(self.serializer_class(qs, many=True).data, status=200)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = Technology(**serializer.data)
        obj.save()
        return Response(data=serializer.data, status=201)



