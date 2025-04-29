from django.contrib.auth import user_logged_in
from django.dispatch import receiver

from shop.utils import get_or_create_cart

"""
Сигналы для обработки корзины покупок при авторизации пользователя.
"""


@receiver(user_logged_in)
def merge_carts_on_login(sender, request, user, **kwargs):
    """
    Объединяет анонимную корзину с корзиной авторизованного пользователя при входе в систему.
    
    Args:
        sender: Отправитель сигнала
        request: HTTP запрос
        user: Авторизованный пользователь
        **kwargs: Дополнительные аргументы
    """
    get_or_create_cart(request)