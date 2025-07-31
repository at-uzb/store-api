from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from storages.backends.s3boto3 import S3Boto3Storage
from django.db.models import DecimalField


def user_upload_path(instance, filename):
    return f"user_{instance.id}/{filename}"


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Users must have a phone number')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=75, blank=True)
    surname = models.CharField(max_length=75, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=20, 
        choices=[('male', 'Male'), 
                 ('female', 'Female')], 
                 blank=True)
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")
        ]
    )
    email = models.EmailField(blank=True, unique=True)
    balance = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    language = models.CharField(max_length=10, default='en')
    photo = models.ImageField(
        upload_to=user_upload_path,
        storage=S3Boto3Storage(),
        # default="profile/default.png"
    )
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number


class PhoneOTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    @property
    def is_expired(self):
        now = timezone.now()
        expiry_time = self.created_at + timedelta(minutes=5)
        print(f"NOW: {now}, CREATED: {self.created_at}, EXPIRY: {expiry_time}")
        return now > expiry_time

    def __str__(self):
        return f"{self.phone_number} - {self.otp}"
