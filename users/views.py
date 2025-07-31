import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PhoneOTP, User
from .serializers import (
    SendOTPSerializer, 
    VerifyOTPSerializer,
    RegisterSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    PreDeletionSerializer,
    DeleteUserSerializer
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from .utils import EskizClient
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes


def generate_otp():
    return str(random.randint(100000, 999999))

class RegisterView(APIView):
    """
    Registers User | returns error if user exists or otp not verified! 
    !!! First create OTP and verify it !!!
    """
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        phone = request.data.get("phone_number")
        
        if User.objects.filter(phone_number=phone).exists():
            return Response(
                {'error': 'User already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            otp = PhoneOTP.objects.get(phone_number=phone)
        except PhoneOTP.DoesNotExist:
            return Response(
                {'error': 'OTP verification required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not otp.is_verified:
            return Response(
                {'error': 'Phone number not verified'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        elif otp.is_expired:
            return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        user = User.objects.create(
            name=validated_data['name'],
            surname=validated_data['surname'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password']) 
        user.is_verified = True
        user.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class SendOTPView(APIView):
    """
    Sends a 6-digit OTP to the provided phone number.
    You can get temp code from response since its paid to send code via phone num.
    But for testing (which is free) You'll get sms
    """
    serializer_class = SendOTPSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            phone = serializer.validated_data['phone_number']

            otp = generate_otp()
            PhoneOTP.objects.update_or_create(
                phone_number=phone,
                defaults={
                    'otp': otp,
                    'is_verified': False,
                    'created_at': timezone.now(),
                }
            )

            eskiz = EskizClient()
            sms = eskiz.send_sms(phone, otp)
            return Response({'message': 'OTP sent successfully', "sms":sms, "temp":otp}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    """
    Verifies the OTP for a phone number.
    """
    serializer_class = VerifyOTPSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone_number']
        otp = serializer.validated_data['otp']

        try:
            otp_obj = PhoneOTP.objects.get(phone_number=phone)
        except PhoneOTP.DoesNotExist:
            return Response({'error': 'Phone number not found'}, status=status.HTTP_404_NOT_FOUND)

        if otp_obj.is_expired:
            return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

        if otp_obj.otp != otp:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        otp_obj.is_verified = True
        otp_obj.save()

        return Response({'message': 'Phone number verified successfully'}, status=status.HTTP_200_OK)
    

class UserDetailView(APIView):
    """
    Returns User Detail
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    """
    Can Update all permitted fields at once or partially
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
    

class ConfirmDeletionView(APIView):
    """First step of Account Deletion where User Confirms deletion and otp is sent"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            otp = generate_otp()
            PhoneOTP.objects.update_or_create(
                phone_number = user.phone_number,
                defaults={
                    'otp': otp,
                    'is_verified': False,
                    'created_at': timezone.now(),
                }
            )

            eskiz = EskizClient()
            sms = eskiz.send_sms(user.phone_number, otp)
            return Response({'message': 'OTP sent successfully', "sms":sms, "temp":otp}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Oops! Error occured '+str(e)}, status=status.HTTP_204_NO_CONTENT)


class PreDeletionView(APIView):
    """
    OTP is verified here for deletion
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PreDeletionSerializer

    def post(self, request):
        serializer = PreDeletionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'OTP verified for account deletion'})



class DeleteUserView(APIView):
    """
    Account will be deleted forever
    Submit password to delete the account permanently.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteUserSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
            
        if not user.check_password(serializer.validated_data['password']):
            return Response({'error': 'Password is incorrect'}, status=400)
            
        user.delete()
        return Response(
            {'message': 'Account has been deleted successfully!'},
            status=200
        )


