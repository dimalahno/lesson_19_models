from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """
    Модель пользователя в системе магазина.

    Расширяет стандартную модель пользователя Django дополнительными полями
    для хранения контактной информации покупателя.

    Attributes:
        email (EmailField): Уникальный email адрес пользователя
        phone_number (CharField): Номер телефона пользователя
        address (TextField): Адрес доставки пользователя
    """

    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес доставки')
    is_active = models.BooleanField(default=False, verbose_name='Аккаунт активен')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Message(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя", blank=False, null=False)
    email = models.EmailField(verbose_name="Электронная почта", blank=False, null=False)
    text = models.TextField(max_length=500, verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self):
        return f"Сообщение от {self.name}"