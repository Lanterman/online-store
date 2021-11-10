from django.urls import path, include

urlpatterns = [
    path('shop/', include(main.urls)),
]
