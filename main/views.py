import django_filters
from django.db.models import Count
from rest_framework import viewsets, mixins, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import *
from main.permissions import AddIfNotParent, IfBasketUser
from main.serializers import *
from main.service import ProductFilter


class ProductViewSets(viewsets.ModelViewSet):
    """
    Список продуктов.
    Дельная информация, добавление, изменение и удаление продукта.
    Добавление комментария.
    Добавление/удаление продукта в/из корзину.
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

    @action(detail=True)
    def add_or_del_product_to_basket(self, request, *args, **kwargs):
        """Добавление/удаление продукта в/из корзину"""
        basket = Basket.objects.get_or_create(user=request.user.username)[0]
        product = self.get_object()
        bas_product = basket.product.all()
        if product in bas_product:
            basket.product.remove(product)
            return Response(data='Товар удален из корзины.', status=status.HTTP_200_OK)

        else:
            basket.product.add(product)
            return Response(data='Товар добавлен в корзину.', status=status.HTTP_200_OK)


class CategoryViewSets(viewsets.ModelViewSet):
    """
    Список категорий.
    Дельная информация, добавление, изменение и удаление категории.
    """
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


class CommentRetrieveViewSets(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """Детальная информация комментария, ответ на комментарий"""
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            if self.get_object().parent:
                return CommentChildrenSerializer
            return CommentDetailSerializer
        if self.action == 'add_comment':
            return CommentCreateSerializer

    def get_permissions(self):
        if self.action == 'add_comment':
            permission_classes = [AddIfNotParent, permissions.IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def add_comment(self, request, *args, **kwargs):
        """Добавление комментария"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            Comment.objects.create(**serializer.validated_data, user_id=request.user.pk,
                                   parent_id=self.get_object().id, product_id=self.get_object().product.id)
            return Response(data={'status': 'Комментарий добавлен', 'info': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(data='Error', status=status.HTTP_404_NOT_FOUND)


class BasketViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Корзина пользователя"""
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()
    permission_classes = [IfBasketUser, permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        basket = Basket.objects.get_or_create(user=self.request.user.username)[0]
        serializer = self.get_serializer(basket)
        return Response(data=serializer.data)
