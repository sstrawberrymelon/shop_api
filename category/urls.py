from django.urls import path, include
from category import views

urlpatterns = [
    path('', views.CategoryViewSet.as_view()),
]
