from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from django.conf import settings
from django.conf.urls.static import static

from category.views import CategoryViewSet
from order.views import OrderApiView
from product.views import ProductViewSet

from .swagger import urlpatterns as doc_urls

router = SimpleRouter()
router.register('category', CategoryViewSet)
router.register('products', ProductViewSet)

urlpatterns = [
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('account.urls')),
    path('api/v1/orders/', OrderApiView.as_view()),
    path('api/v1/', include(router.urls))
] + doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
