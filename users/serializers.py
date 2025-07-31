from rest_framework import serializers
from .models import User, PhoneOTP
from django.core.validators import EmailValidator


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=15)
    surname = serializers.CharField(max_length=15)
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        validators=[EmailValidator(message="Enter a valid email address.")],
        required=True)


    def validate_phone_number(self, value):
        if not value.startswith('+998') or not value[1:].isdigit() or len(value) != 13:
            raise serializers.ValidationError("Invalid Uzbekistan phone number format.")
        return value
     
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data


class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=15,
        help_text="Uzbekistan phone number, e.g. +998901234567"
    )


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=15,
        help_text="Phone number that received the OTP"
    )
    otp = serializers.CharField(
        max_length=6,
        help_text="6-digit OTP sent to the phone number"
    )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'name', 'surname', 'birth_date',
            'gender', 'phone_number', 'email', 'balance',
            'language', 'photo', 'is_admin', 'is_superuser'
        ]
        read_only_fields = ['id', 'is_superuser', 'phone_number']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match")
        return data

   
class PreDeletionSerializer(serializers.Serializer):    
    otp = serializers.CharField()

    def validate(self, data):
        otp = data.get("otp")
        user = self.context['request'].user
        phone = user.phone_number
        try:
            otp_obj = PhoneOTP.objects.get(phone_number=phone)
        except PhoneOTP.DoesNotExist:
            raise serializers.ValidationError("OTP not found for this phone number")

        if otp_obj.is_expired:
            raise serializers.ValidationError("OTP has expired")

        if otp_obj.otp != otp:
            raise serializers.ValidationError("Invalid OTP")
        otp_obj.is_verified = True
        return data


class DeleteUserSerializer(serializers.Serializer):
    password =  serializers.CharField(required=True)
