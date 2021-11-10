from django.contrib.auth.models import User
from django.db.models import Count
from django.test import TestCase

from main.serializers import *
from main.models import Category, Product, Comment


class ProductDetailSerializerTestCase(TestCase):
    def test_valid(self):
        category = Category.objects.create(name='test', slug='test')
        product_1 = Product.objects.create(name='product_1', slug='product_1', price=2400, category=category)
        product_2 = Product.objects.create(name='product_2', slug='product_2', price=2200, category=category,
                                           stock_in=True)
        data_1 = ProductDetailSerializer(product_1, context={'request': None}).data
        data_2 = ProductDetailSerializer(product_2, context={'request': None}).data
        self.assertEqual(len(data_1), 8)
        self.assertEqual(data_1['stock_in'], False)
        self.assertEqual(len(data_2), 8)
        self.assertEqual(data_2['stock_in'], True)
        self.assertEqual(data_2['category']['url'] == '/category/test/', data_1['category']['url'] == '/category/test/')


class ProductListSerializerTestCase(TestCase):
    def test_valid(self):
        category = Category.objects.create(name='test', slug='test')
        product_1 = Product.objects.create(name='product_1', slug='product_1', price=2400, category=category)
        product_2 = Product.objects.create(name='product_2', slug='product_2', price=2200, category=category,
                                           stock_in=True)
        data = ProductListSerializer([product_1, product_2], context={'request': None}, many=True).data
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['stock_in'], False)
        self.assertEqual(data[1]['stock_in'], True)
        self.assertEqual(data[0]['category']['url'], '/shop/category/test/')
        self.assertEqual(data[1]['category']['url'], '/shop/category/test/')


class ProductCreateUpdateSerializerTestCase(TestCase):
    def test_valid(self):
        category = Category.objects.create(name='test', slug='test')
        product_1 = Product.objects.create(name='product_1', slug='product_1', price=2400, category=category)
        data = ProductCreateUpdateSerializer(product_1).data
        self.assertEqual(len(data), 6)
        self.assertEqual(data['stock_in'], False)


class CategoryListSerializerTestCase(TestCase):
    def test_valid(self):
        cat = Category.objects.create(name='test_1', slug='test_1')
        Category.objects.create(name='test_2', slug='test_2')
        Product.objects.create(name='product_1', slug='product_1', price=2400, category=cat)
        category = Category.objects.all().annotate(number_of_products=Count('product_set'))
        data = CategoryListSerializer(category, context={'request': None}, many=True).data
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['number_of_products'], 0)
        self.assertEqual(data[1]['number_of_products'], 1)
        self.assertEqual(data[0]['url'], '/shop/category/test_2/')
        self.assertEqual(data[1]['url'], '/shop/category/test_1/')


class CategoryDetailSerializerTestCase(TestCase):
    def test_valid(self):
        cat_1 = Category.objects.create(name='test_1', slug='test_1')
        Category.objects.create(name='test_2', slug='test_2')
        Product.objects.create(name='product_1', slug='product_1', price=2400, category=cat_1)
        category = Category.objects.all().annotate(number_of_products=Count('product_set'))
        data_1 = CategoryDetailSerializer(category[0], context={'request': None}).data
        data_2 = CategoryDetailSerializer(category[1], context={'request': None}).data
        self.assertEqual(len(data_1), 4)
        self.assertEqual(data_1['number_of_products'], 1)
        self.assertEqual(len(data_2), 4)
        self.assertEqual(data_2['number_of_products'], 0)
        self.assertEqual(len(data_1['product_set']) == 1, len(data_2['product_set']) == 0)
        self.assertEqual(data_1['product_set'][0]['url'], '/shop/product/product_1/')


class CategoryCreateUpdateSerializerTestCase(TestCase):
    def test_valid(self):
        category = Category.objects.create(name='test', slug='test')
        data = CategoryCreateUpdateSerializer(category).data
        self.assertEqual(len(data), 1)
        self.assertEqual(data['name'], 'test')


class CommentCreateSerializerTestCase(TestCase):
    def test_valid(self):
        category = Category.objects.create(name='test', slug='test')
        product = Product.objects.create(name='product_1', slug='product_1', price=2400, category=category)
        user = User.objects.create(username='user')
        comment_1 = Comment.objects.create(user=user, product=product, description='yes')
        comment_2 = Comment.objects.create(user=user, product=product, parent=comment_1, description='no')
        data_1 = CommentCreateSerializer(comment_1).data
        data_2 = CommentCreateSerializer(comment_2).data
        self.assertEqual(len(data_1) == 1, len(data_2) == 1)
        self.assertEqual(data_1['description'], 'yes')
        self.assertEqual(data_2['description'], 'no')


class CommentDetailSerializerTestCase(TestCase):
    def test_valid(self):
        category = Category.objects.create(name='test', slug='test')
        product = Product.objects.create(name='product_1', slug='product_1', price=2400, category=category)
        user = User.objects.create(username='user')
        comment_1 = Comment.objects.create(user=user, product=product, description='yes')
        comment_2 = Comment.objects.create(user=user, product=product, parent=comment_1, description='no')
        data_1 = CommentDetailSerializer(comment_1, context={'request': None}).data
        data_2 = CommentDetailSerializer(comment_2, context={'request': None}).data
        self.assertEqual(len(data_1) == 4, len(data_2) == 4)
        self.assertEqual(data_1['description'], 'yes')
        self.assertEqual(data_2['description'], 'no')
        self.assertEqual(len(data_1['children']) == 1, len(data_2['children']) == 0)
