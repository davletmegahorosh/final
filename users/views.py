from django.conf import settings
from rest_framework.generics import get_object_or_404

from .models import ConfirmationCode
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from final.settings import EMAIL_HOST_USER
from .models import CustomUsers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Отправка электронной почты с кодом подтверждения
            confirmation_code = user.confirmation_code
            subject = 'Confirmation code'
            message = f'Your confirmation code is: {confirmation_code}'
            from_email = EMAIL_HOST_USER  # Укажите ваш отправительский email
            recipient_list = [user.email]

            # Ваш код отправки почты (send_mail)...
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()


class VerifyAccount(APIView):
    serializer_class = VerifyAccountSerializer

    def post(self, request):
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.validated_data['confirmation_code']

            user = get_object_or_404(CustomUsers, confirmation_code=confirmation_code, is_active=False)

            # Activate the user in CustomUser model
            user.is_active = True
            user.save()

            return Response({'message': 'Email confirmed successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CustomUserTokenRefreshView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            return Response({'access': access_token,
                             'refresh': token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            # Проверка старого пароля
            if not user.check_password(old_password):
                return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            # Установка нового пароля
            user.set_password(new_password)
            user.save()

            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUsernameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangeUsernameSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            new_username = serializer.data.get("new_username")

            user.username = new_username
            user.save()

            return Response({"detail": "Username changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = ForgotPasswordSerializer
    queryset = User.objects.all()  # Use the User queryset here
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Get a QuerySet of all users with the specified email address
        users = User.objects.filter(email=email)

        if not users.exists():
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Generate a confirmation code
        confirmation_code = get_random_string(length=4, allowed_chars='0123456789')

        # Create a ConfirmationCode object for the user
        user = users[0]  # Assuming that the email is unique
        ConfirmationCode.objects.create(user=user, code=confirmation_code)

        # Send the code to the user's email
        subject = 'Confirmation Code'
        message = f'Your confirmation code is: {confirmation_code}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return Response({'message': 'Confirmation code sent successfully.'})


class ResetPasswordView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            confirmation_code = serializer.validated_data.get("confirmation_code")
            new_password = serializer.validated_data.get("new_password")

            try:
                confirmation = ConfirmationCode.objects.get(user__email=email, code=confirmation_code)
            except ConfirmationCode.DoesNotExist:
                return Response({"detail": "Invalid or expired confirmation code."}, status=status.HTTP_400_BAD_REQUEST)

            user = confirmation.user
            user.set_password(new_password)
            user.save()

            confirmation.delete()

            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)