from email.mime import image

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    """
    Model representing a category in the shop system.
    
    This model implements a hierarchical category structure where each category can have
    a parent category and multiple subcategories. It is used for organizing products
    in the shop into a tree-like structure.
    
    Attributes:
        name (CharField): The name of the category with maximum length of 256 characters.
        description (TextField): Optional description of the category.
        parent (ForeignKey): Reference to parent category, can be null for top-level categories.
            Creates a self-referential relationship allowing hierarchical structure.
    """
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name='Родительская категория'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Model representing a product in the shop system.

    This model stores information about products available in the shop,
    including their details, pricing, inventory, and categorization.

    Attributes:
        name (CharField): The name of the product.
        description (TextField): Detailed description of the product.
        price (DecimalField): Product price with decimal precision.
        stock (IntegerField): Current quantity available in stock.
        image (ImageField): Product image file, optional.
        category (ForeignKey): Reference to the product's category.
        created_at (DateTimeField): Timestamp of when the product was added.
    """
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена'
    )
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Количество на складе'
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        unique_together = ('name', 'category')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'В обработке'),
        ('shipping', 'Доставляется'),
        ('delivered', 'Доставлено'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing', verbose_name='Статус')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая стоимость')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.id} от {self.user.username}'

    def update_total_price(self):
        total = sum(item.total_price() for item in self.items.all())
        self.total_price = total
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    def total_price(self):
        return self.product.price * self.quantity

class Review(models.Model):
    """
    Модель отзыва в системе магазина.
    
    Хранит информацию об отзывах пользователей на товары, включая оценку
    и текстовый комментарий. Один пользователь может оставить только один отзыв
    на конкретный товар.
    
    Attributes:
        product (ForeignKey): Товар, к которому относится отзыв
        user (ForeignKey): Пользователь, оставивший отзыв
        rating (PositiveSmallIntegerField): Оценка товара от 1 до 5
        comment (TextField): Текстовый отзыв о товаре
        created_at (DateTimeField): Дата и время создания отзыва
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', verbose_name='Пользователь')
    rating = models.PositiveSmallIntegerField(verbose_name='Оценка')
    comment = models.TextField(blank=True, verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        # Один пользователь — один отзыв на товар
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв {self.user.username} о {self.product.name} ({self.rating}/5)'

    def clean(self):
        from django.core.exceptions import ValidationError
        if not (1 <= self.rating <= 5):
            raise ValidationError('Оценка должна быть от 1 до 5.')
        
class Cart(models.Model):
    """
    Модель корзины покупок в системе магазина.
    
    Хранит информацию о корзине каждого пользователя и связанных с ней товарах.
    Один пользователь может иметь только одну корзину.
    
    Attributes:
        user (OneToOneField): Пользователь, которому принадлежит корзина.
        created_at (DateTimeField): Дата и время создания корзины.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'

class CartItem(models.Model):
    """
    Модель элемента корзины в системе магазина.
    
    Хранит информацию о товарах, добавленных в корзину покупок,
    включая количество каждого товара. Связывает корзину с конкретными
    товарами и их количеством.
    
    Attributes:
        cart (ForeignKey): Корзина, к которой относится элемент
        product (ForeignKey): Товар в корзине
        quantity (PositiveIntegerField): Количество единиц товара
    """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    def get_total_price(self):
        return self.product.price * self.quantity