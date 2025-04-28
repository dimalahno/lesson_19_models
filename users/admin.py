from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "phone_number", "address", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Персональная информация", {"fields": ("phone_number", "address")}),
        ("Права доступа", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "phone_number", "address", "is_staff", "is_active"),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

