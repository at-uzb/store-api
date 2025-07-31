from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PhoneOTP

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('phone_number', 'name', 'surname', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('name', 'surname', 'birth_date', 'gender', 'language', 'balance')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Photo', {'fields': ('photo',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)

admin.site.register(User, UserAdmin)
admin.site.register(PhoneOTP)
