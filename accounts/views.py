from .serializers import RegistrationSerializer, AuthUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tokens import email_verification_token
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken. views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import update_last_login


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


register = RegistrationView.as_view()


class ActivateView(APIView):
    def get_user_from_email_verification_token(self, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                get_user_model().DoesNotExist):
            return None

        if user is not None \
                and \
                email_verification_token.check_token(user, token):
            return user

        return None

    def get(self, request, uidb64, token):
        user = self.get_user_from_email_verification_token(
            uidb64, token)
        if user is None:
            return Response({'status': 'failed', 'message': 'Invalid'})
        user.is_active = True
        user.customer.email_verified = True
        user.customer.email_verified_at = timezone.now()
        user.customer.save()
        user.save()
        return Response({'status': 'success', 'message': 'Valid'})


activate = ActivateView.as_view()


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

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': str(user)
        }, status=status.HTTP_201_CREATED)

    def delete(self, request):
        request.user.auth_token.delete()
        return Response({'detail': 'Auth token is expired now. You need to obtain a new token to be used in the subsequent requests.'}, status=status.HTTP_205_RESET_CONTENT)


auth_tokens = AuthToken.as_view()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def auth_user(request):
    serializer = AuthUserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
