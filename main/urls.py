from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import *

router = DefaultRouter()
router.register(r'product', ProductViewSets)
router.register(r'category', CategoryViewSets, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
