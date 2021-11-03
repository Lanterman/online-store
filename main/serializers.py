from rest_framework import serializers

from main.models import *


class ProductCategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail', lookup_field='slug')

    class Meta:
        model = Category
        fields = ('url', 'name')


class ProductCommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='slug')

    class Meta:
        model = Product
        fields = ('url', 'name')


class CatProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='slug')

    class Meta:
        model = Product
        fields = ('url', 'name', 'slug', 'photo', 'price', 'stock_in')


class CommentChildrenSerializer(serializers.ModelSerializer):
    """Дочерние комментарии"""
    # user = UserSerializer()

    class Meta:
        model = Comment
        fields = ('description', 'user', 'date')


class FilterCommentSerializer(serializers.ListSerializer):
    """Фильтрация комментариев"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CommentSerializer(serializers.ModelSerializer):
    """Отзыв(-ы)"""
    # url = serializers.HyperlinkedIdentityField(view_name='comment-detail')
    # user = UserSerializer()
    children = CommentChildrenSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentSerializer
        model = Comment
        fields = ('description', 'user', 'children', 'date')


# main

class ProductDetailSerializer(serializers.ModelSerializer):
    """Детальная информация продуктов"""
    category = ProductCategorySerializer()
    comments_set = CommentSerializer(many=True)

    class Meta:
        model = Product
        fields = ('name', 'slug', 'photo', 'price', 'stock_in', 'category', 'description', 'comments_set')


class ProductListSerializer(serializers.ModelSerializer):
    """Список всех продуктов"""
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='slug')
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = ('url', 'name', 'slug', 'photo', 'price', 'stock_in', 'category', 'description')


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Создание/обновление продукта"""
    class Meta:
        model = Product
        fields = ('name', 'photo', 'price', 'stock_in', 'category', 'description')


class CategoryListSerializer(serializers.ModelSerializer):
    """Список всех категорий"""
    url = serializers.HyperlinkedIdentityField(view_name='category-detail', lookup_field='slug')
    number_of_products = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ('url', 'name', 'slug', 'number_of_products')


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Детальная информация категории"""
    number_of_products = serializers.IntegerField()
    product_set = CatProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'number_of_products', 'product_set')


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    """Создание/обновление категории"""
    class Meta:
        model = Category
        fields = ('name',)


class CommentCreateSerializer(serializers.ModelSerializer):
    """Создание отзыва"""
    class Meta:
        model = Comment
        fields = ('description',)
