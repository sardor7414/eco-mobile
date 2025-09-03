import random
import string
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

User = get_user_model()

def send_sms(phone, code):
    print(f"SMS to {phone}: Your reset code is {code}")

class ForgotPasswordView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({"error": "Bunday foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        code = str(random.randint(100000, 999999))
        user.reset_code = code
        user.save()

        send_sms(phone, code)  # SMS yuborish

        return Response({"message": "Tasdiqlash kodi yuborildi"})


class VerifyResetCodeView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        code = request.data.get("code")

        try:
            user = User.objects.get(phone=phone, reset_code=code)
        except User.DoesNotExist:
            return Response({"error": "Noto‘g‘ri kod"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_reset_verified = True
        user.save()

        return Response({"message": "Kod tasdiqlandi"})


# class ResetPasswordView(APIView):
#     def post(self, request):
#         phone = request.data.get("phone")
#         new_password = request.data.get("new_password")
#
#         try:
#             user = User.objects.get(phone=phone, is_reset_verified=True)
#         except User.DoesNotExist:
#             return Response({"error": "Avval kodni tasdiqlang"}, status=status.HTTP_400_BAD_REQUEST)
#
#         user.set_password(new_password)
#         user.reset_code = None
#         user.is_reset_verified = False
#         user.save()
#
#         return Response({"message": "Parol muvaffaqiyatli o‘zgartirildi"})

class ResetPasswordView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        new_password = request.data.get("new_password")

        try:
            user = User.objects.get(phone=phone, is_reset_verified=True)
        except User.DoesNotExist:
            return Response({"error": "Avval kodni tasdiqlang"}, status=status.HTTP_400_BAD_REQUEST)

        # Agar parol yuborilmagan bo‘lsa, random parol generatsiya qilamiz
        if not new_password:
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        user.set_password(new_password)
        user.reset_code = None
        user.is_reset_verified = False
        user.save()

        return Response({
            "message": "Parol muvaffaqiyatli o‘zgartirildi",
            "new_password": new_password
        })

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)