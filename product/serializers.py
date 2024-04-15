from django.db.models import Avg
from rest_framework import serializers

from category.models import Category
from .models import Product


class PoductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Product
        fields = ('id', 'owner', 'owner_email', 'title', 'price', 'image')

    def representation(self, instance):
        repr = super().to_representation(instance)
        try:
            repr['rating_avg'] = round(instance.ratings.aggregate(Avg('rating'))['rating__avg'], 1)
        except TypeError:
            repr['rating_avg'] = None
        return repr


class ProductSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        try:
            repr['rating_avg'] = round(instance.ratings.aggregate(Avg('rating'))['rating__avg'], 1)
        except AttributeError:
            repr['rating_avg'] = None
        return repr
