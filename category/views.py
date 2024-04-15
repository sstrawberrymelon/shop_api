from django.shortcuts import render
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from . import serializers
from category.models import Category


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerialaizer

    def get_permission(self):
        if self.action in ('retrieve', 'list'):
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

