from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'

# Список товаров
urlpatterns = []

# Добавляем возможность отображения изображений
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)