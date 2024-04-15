from rest_framework import serializers
from .models import Category

class CategorySerialaizer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Category
        fields = '__all__'