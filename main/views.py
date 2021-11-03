import django_filters
from django.db.models import Count
from rest_framework import viewsets, mixins, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import Product, Comment
from main.serializers import *
from main.service import ProductFilter


class ProductViewSets(viewsets.ModelViewSet):
    """
    Список продуктов.
    Дельная информация, добавление, изменение и удаление продукта.
    Добавление комментария.
    """
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name']
    ordering_fields = ['name', 'price']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        if self.action == 'retrieve':
            return ProductDetailSerializer
        if self.action == 'add_comment':
            return CommentCreateSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return ProductCreateUpdateSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'create', 'destroy'):
            permission_classes = [permissions.IsAdminUser]
        elif self.action in ('list', 'retrieve'):
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        product = serializer.save()
        product.slug = product.name
        product.save()

    def perform_update(self, serializer):
        product = serializer.save()
        product.slug = product.name
        product.save()

    @action(detail=True, methods=['post'])
    def add_comment(self, request, *args, **kwargs):
        """Добавление комментария"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            Comment.objects.create(**serializer.validated_data, user_id=request.user.pk,
                                   product_id=self.get_object().id)
            return Response(data={'status': 'Комментарий добавлен', 'info': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(data='Error', status=status.HTTP_404_NOT_FOUND)


class CategoryViewSets(viewsets.ModelViewSet):
    """Категории"""
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['number_of_products']
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Category.objects.all().annotate(number_of_products=Count('product_set'))
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return CategoryCreateUpdateSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'create', 'destroy'):
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        category = serializer.save()
        category.slug = category.name
        category.save()

    def perform_update(self, serializer):
        category = serializer.save()
        category.slug = category.name
        category.save()
