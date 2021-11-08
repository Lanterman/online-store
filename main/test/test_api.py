from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from main.models import *
from main.serializers import *


# class ProductViewSetsTestCase(APITestCase):
#     def setUp(self):
#         category = Category.objects.create(name='test', slug='test')
#         self.product_1 = Product.objects.create(name='product_1', slug='product_1', price=2400, category=category)
#         self.product_2 = Product.objects.create(name='product_2', slug='product_2', price=2200, category=category,
#                                            stock_in=True)
#
#     def test_get(self):
#
#         data_1 = ProductDetailSerializer(self.product_1, context={'request': None}).data
#         data_2 = ProductDetailSerializer(self.product_2, context={'request': None}).data
#         url_1 = reverse('product-detail', kwargs={'slug': self.product_1.slug})
#         url_2 = reverse('product-detail', kwargs={'slug': self.product_2.slug})
#         response_1 = self.client.get(url_1)
#         response_2 = self.client.get(url_2)
#         self.assertEqual(response_1.status_code, status.HTTP_200_OK)
#         self.assertEqual(response_2.status_code, status.HTTP_200_OK)