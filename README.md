# Интернет-магазин (Django)

## Описание проекта
Простой интернет-магазин на Django, который отображает список товаров и детальную информацию о каждом из них.

## Функционал
- Отображение списка заказов, товаров, корзины, пользователей 
- Просмотр детальной информации
- Админ-панель для управления

## Установка и запуск

### 1. Клонирование репозитория
```sh
git clone https://github.com/dimalahno/lesson_19_models.git
cd eshop
```

### 2. Создание виртуального окружения
```sh
python -m venv venv
source venv/bin/activate  # Для macOS/Linux
venv\Scripts\activate  # Для Windows
```

### 3. Установка зависимостей
```sh
pip install -r requirements.txt
```

### 4. Настройка базы данных
Примените миграции:
```sh
python manage.py migrate
```

### 5. Создание суперпользователя
```sh
python manage.py createsuperuser
```

### 6. Запуск сервера
```sh
python manage.py runserver
```

### 7. Доступ к админке
Перейдите в браузере: `http://127.0.0.1:8000/admin/`


# Работа с shell
python manage.py shell
from shop.models import Category, Product

## Создание категорий
electronics = Category.objects.create(name='Электроника', description='Гаджеты и устройства')
clothing = Category.objects.create(name='Одежда')
books = Category.objects.create(name='Книги')

## Вложенная категория
smartphones = Category.objects.create(name='Смартфоны', parent=electronics)

## Товары для электроники
Product.objects.create(
    name='iPhone 14',
    description='Современный смартфон Apple',
    price=999.99,
    stock=10,
    category=smartphones
)

Product.objects.create(
    name='Наушники Sony WH-1000XM4',
    description='Беспроводные наушники с шумоподавлением',
    price=299.99,
    stock=25,
    category=electronics
)

## Товары для одежды
Product.objects.create(
    name='Футболка',
    description='Белая хлопковая футболка',
    price=19.99,
    stock=100,
    category=clothing
)

## Товары для книг
Product.objects.create(
    name='1984',
    description='Антиутопический роман Джорджа Оруэлла',
    price=9.99,
    stock=50,
    category=books
)

## Проверки
Category.objects.all()
Product.objects.all()

## Получим категорию по имени
category = Category.objects.get(name='Электроника')

## Получим все товары, принадлежащие этой категории
products = Product.objects.filter(category=category)

## Выведем
for product in products:
    print(product.name, product.price)

## Получаем все подкатегории
subcategories = Category.objects.filter(parent=category)

## Получаем товары из категории и всех её подкатегорий
products = Product.objects.filter(category__in=[category] + list(subcategories))

## Получить отзывы
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='admin')
product = Product.objects.get(name='iPhone 14')