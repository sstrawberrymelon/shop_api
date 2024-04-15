from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action

from rating.serializers import RatingSerializer
from .models import Product
from . import serializers
from .permissions import IsAuthor, IsAuthorOrAdmin


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductSerializer
        return serializers.ProductSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update'):
            return [IsAuthor()]
        elif self.action in 'destroy':
            return [IsAuthorOrAdmin()]
        return [permissions.IsAuthenticated()]

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def rating(self, request, pk):
        product = self.get_object()
        user = request.user
        is_rating = product.ratings.filter(owner=user).exists()
        # P.s.: is_XXX возвращает всегда bool

        if request.method == 'GET':
            ratings = product.ratings.all()
            serializer = RatingSerializer(ratings, many=True)
            return Response(serializer.data, status=200)
        elif request.method == 'POST':
            if is_rating:
                return Response({'msg': 'Already rated this product'},
                                status=400)
            data = request.data
            serializer = RatingSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user, product=product)
            return Response(serializer.data, status=201)
        else:
            if not is_rating:
                return Response({'msg': 'Not rated this product'},
                                status=400)
            # product.ratings.remove(user)
            # return Response(status=204)
            rating = product.ratings.get(owner=user)
            rating.delete()
            return Response({'msg': 'Deleted!'}, status=204)
