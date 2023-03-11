from rest_framework.views import APIView
from .serializers import RegistrationSerializer, PasswordSerializer, AuthUserSerializer
from rest_framework.response import Response
from rest_framework import status
from .models.custom_users import Customer
from .signals import password_forgotten
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from .tokens import email_verification_token, password_reset_token
from django.utils import timezone
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import update_last_login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateView(APIView):
    def get(self, request, uidb64, token):
        user = _get_user(uidb64, token, email_verification_token)
        if user is None:
            return Response({'detail': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.email_verified = True
        user.email_verified_at = timezone.now()
        user.save()
        return Response({'detail': 'Activated Successfully'}, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        if email is None:
            return Response({"email": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Customer, email=email)
        try:
            password_forgotten.send(self.__class__, instance=user)
            return Response({'detail': 'Reset Password Link Sent Successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Something went wrong while trying to send the email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordResetConfirmView(APIView):
    def patch(self, request, uidb64, token):
        user = _get_user(uidb64, token, password_reset_token)
        if user is None:
            return Response({'detail': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password1'])
            user.save()
            return Response({'detail': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors)


class AuthToken(ObtainAuthToken):
    def get_permissions(self):
        if self.request.method in ['DELETE']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        update_last_login(None, token.user)

        response = AuthUserSerializer(user).data
        response['token'] = token.key

        return Response(response, status=status.HTTP_201_CREATED)

    def delete(self, request):
        request.user.auth_token.delete()
        return Response({'detail': 'Auth token is expired now. You need to obtain a new token to be used in the subsequent requests.'}, status=status.HTTP_205_RESET_CONTENT)


@ api_view(['GET'])
@ permission_classes([IsAuthenticated])
def auth_user(request):
    serializer = AuthUserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


def _get_user(uidb64, token, token_type):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(Customer, pk=uid)

    if token_type.check_token(user, token):
        return user

    return None
