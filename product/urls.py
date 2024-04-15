from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ProductViewSet.as_view()),
]