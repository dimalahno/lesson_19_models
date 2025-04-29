from django.shortcuts import render

from shop.utils import get_or_create_cart


def add_to_cart(request, product_id):
    cart = get_or_create_cart(request)
    # Далее: добавление товара в cart.items