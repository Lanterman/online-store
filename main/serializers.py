from rest_framework import serializers

from main.models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    comments_set = CommentSerializer(many=True)

    class Meta:
        model = Product
        fields = ('name', 'slug', 'photo', 'price', 'stock_in', 'category', 'description', 'comments_set')


class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='slug')

    class Meta:
        model = Product
        fields = ('url', 'name', 'slug', 'photo', 'price', 'stock_in', 'description')


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'photo', 'price', 'stock_in', 'category', 'description')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('description',)
