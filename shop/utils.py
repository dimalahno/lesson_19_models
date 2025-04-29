from shop.models import Cart


def get_or_create_cart(request):
    """
    Получает существующую или создает новую корзину для пользователя.
    Для авторизованных пользователей привязывает корзину к аккаунту.
    Для неавторизованных пользователей создает сессионную корзину.
    При авторизации объединяет товары из сессионной корзины с корзиной пользователя.
    """

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Если у сессионной корзины есть товары — объединяем:
        session_key = request.session.session_key
        if session_key:
            try:
                session_cart = Cart.objects.get(session_key=session_key, user=None)
                for item in session_cart.items.all():
                    existing = cart.items.filter(product=item.product).first()
                    if existing:
                        existing.quantity += item.quantity
                        existing.save()
                    else:
                        item.cart = cart
                        item.save()
                session_cart.delete()
            except Cart.DoesNotExist:
                pass
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key, user=None)
    return cart