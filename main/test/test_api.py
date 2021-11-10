import json

from django.db.models import Count
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory,  APIClient

from main.models import *
from main.serializers import *


class ProductViewSetsTestCase(APITestCase):
    def setUp(self):
        self.just_user = User.objects.create_user(username='just_user', password='password')
        self.super_user = User.objects.create_superuser(username='super_user', password='password')
        self.just_token = Token.objects.create(user=self.just_user)
        self.super_token = Token.objects.create(user=self.super_user)
        self.category = Category.objects.create(name='test', slug='test')
        self.product_1 = Product.objects.create(name='product_1', slug='product_1', price=2400, category=self.category)
        self.product_2 = Product.objects.create(name='product_2', slug='product_2', price=2200, category=self.category,
                                                stock_in=True)
        self.basket = Basket.objects.create(user=self.just_user)

    def test_get_list(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('product-list'))
        url = reverse('product-list')
        response = self.client.get(url)
        serializer_data = ProductListSerializer([self.product_2, self.product_1], many=True,
                                                context={'request': request}).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_retrieve(self):
        factory = APIRequestFactory()
        request_1 = factory.get(reverse('product-detail', kwargs={'slug': self.product_1.slug}))
        request_2 = factory.get(reverse('product-detail', kwargs={'slug': self.product_2.slug}))
        url_1 = reverse('product-detail', kwargs={'slug': self.product_1.slug})
        url_2 = reverse('product-detail', kwargs={'slug': self.product_2.slug})
        response_1 = self.client.get(url_1)
        response_2 = self.client.get(url_2)
        serializer_data_1 = ProductDetailSerializer(self.product_1, context={'request': request_1}).data
        serializer_data_2 = ProductDetailSerializer(self.product_2, context={'request': request_2}).data
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data_1, response_1.data)
        self.assertEqual(serializer_data_2, response_2.data)

    def test_post_add_comment(self):
        client = APIClient()
        url = f'/shop/product/{self.product_1.slug}/add_comment/'
        data = {'description': 'test'}
        response = client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.just_token.key)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_create(self):
        client = APIClient()
        url = reverse('product-list')
        data = {'name': 'product_3', 'slug': 'product_3', 'category': self.category.id}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Product.objects.count(), 2)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.just_token.key)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 2)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(Product.objects.get(name='product_3').name, 'product_3')

    def test_post_update(self):
        client = APIClient()
        url = reverse('product-detail', kwargs={'slug': self.product_1.slug})
        data = {'name': 'product_4', 'slug': 'product_4', 'category': self.category.id}
        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.just_token.key)
        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Product.objects.count(), 2)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 2)
        self.assertFalse(Product.objects.filter(name='product_1'))
        self.assertTrue(Product.objects.get(name='product_4'))

    def test_get_destroy(self):
        client = APIClient()
        url = reverse('product-detail', kwargs={'slug': self.product_1.slug})
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Product.objects.filter(name='product_1'))
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.just_token.key)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(name='product_1'))
        self.assertEqual(Product.objects.count(), 2)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)
        self.assertFalse(Product.objects.filter(name='product_1'))


class CategoryViewSetsTestCase(APITestCase):
    def setUp(self):
        self.just_user = User.objects.create_user(username='just_user', password='password')
        self.super_user = User.objects.create_superuser(username='super_user', password='password')
        self.just_token = Token.objects.create(user=self.just_user)
        self.super_token = Token.objects.create(user=self.super_user)
        category = Category.objects.create(name='category_1', slug='category_1')
        Category.objects.create(name='category_2', slug='category_2')
        self.product_1 = Product.objects.create(name='product_1', slug='product_1', price=2400, category=category)
        self.categories = Category.objects.all().annotate(number_of_products=Count('product_set'))

    def test_get_list(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('category-list'))
        url = reverse('category-list')
        response = self.client.get(url)
        serializer_data = CategoryListSerializer(self.categories, many=True,
                                                 context={'request': request}).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_get_retrieve(self):
        factory = APIRequestFactory()
        request_1 = factory.get(reverse('category-detail', kwargs={'slug': self.categories[1].slug}))
        request_2 = factory.get(reverse('category-detail', kwargs={'slug': self.categories[0].slug}))
        url_1 = reverse('category-detail', kwargs={'slug': self.categories[1].slug})
        url_2 = reverse('category-detail', kwargs={'slug': self.categories[0].slug})
        response_1 = self.client.get(url_1)
        response_2 = self.client.get(url_2)
        serializer_data_1 = CategoryDetailSerializer(self.categories[1], context={'request': request_1}).data
        serializer_data_2 = CategoryDetailSerializer(self.categories[0], context={'request': request_2}).data
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data_1, response_1.data)
        self.assertEqual(serializer_data_2, response_2.data)

    # def test_post_create(self):
    #     client = APIClient()
    #     url = reverse('product-list')
    #     data = {'name': 'product_3', 'slug': 'product_3', 'category': self.category.id}
    #     response = client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertEqual(Product.objects.count(), 2)
    #     client.credentials(HTTP_AUTHORIZATION='Token ' + self.just_token.key)
    #     response = client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(Product.objects.count(), 2)
    #     client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
    #     response = client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Product.objects.count(), 3)
    #     self.assertEqual(Product.objects.get(name='product_3').name, 'product_3')

    # def test_post_update(self):
    #     client = APIClient()
    #     url = reverse('product-detail', kwargs={'slug': self.product_1.slug})
    #     data = {'name': 'product_4', 'slug': 'product_4', 'category': self.category.id}
    #     response = client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     client.credentials(HTTP_AUTHORIZATION='Token ' + self.just_token.key)
    #     response = client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(Product.objects.count(), 2)
    #     client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
    #     response = client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(Product.objects.count(), 2)
    #     self.assertFalse(Product.objects.filter(name='product_1'))
    #     self.assertTrue(Product.objects.get(name='product_4'))
    #
    # def test_get_destroy(self):
    #     client = APIClient()
    #     url = reverse('product-detail', kwargs={'slug': self.product_1.slug})
    #     response = client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertTrue(Product.objects.filter(name='product_1'))
    #     client.credentials(HTTP_AUTHORIZATION='Token ' + self.just_token.key)
    #     response = client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertTrue(Product.objects.filter(name='product_1'))
    #     self.assertEqual(Product.objects.count(), 2)
    #     client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
    #     response = client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Product.objects.count(), 1)
    #     self.assertFalse(Product.objects.filter(name='product_1'))

# url = reverse('category-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

# url_1 = reverse('category-detail', kwargs={'slug': category[1].slug})
# url_2 = reverse('category-detail', kwargs={'slug': category[0].slug})
# response_1 = self.client.get(url_1)
# response_2 = self.client.get(url_2)
# self.assertEqual(response_1.status_code, status.HTTP_200_OK)
# self.assertEqual(response_2.status_code, status.HTTP_200_OK)

# url = reverse('category-list')
# response = self.client.post(url)
# self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
