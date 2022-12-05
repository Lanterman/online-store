from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'product', ProductViewSets, basename='product')
router.register(r'category', CategoryViewSets, basename='category')
router.register(r'comment', CommentRetrieveViewSets)
router.register(r'basket', BasketViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth_html/', auth),
]
