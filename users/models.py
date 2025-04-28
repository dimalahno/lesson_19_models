from django.contrib.auth.models import AbstractUser
from django.db import models

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
    address = models.TextField(blank=True, null=True, verbose_name='Адрес')

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