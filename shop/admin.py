from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from shop.models import Category, Product, OrderItem, Order, Review, CartItem, Cart


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('name', 'parent',)
    search_fields = ('name', 'parent',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_price')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity')
    can_delete = False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]

    def total_price(self, obj):
        total = sum(item.get_total_price() for item in obj.items.all())
        return format_html('<b>{:.2f} ₽</b>', total)

    total_price.short_description = 'Сумма корзины'

    def clear_cart(self, request, queryset):
        for cart in queryset:
            cart.items.all().delete()
        self.message_user(request, "Выбранные корзины очищены.")

    clear_cart.short_description = "Очистить выбранные корзины"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')