from django.contrib import admin
from django.urls import path

from .views import ProductViewSet, UserAPIView

#Django-URL-Konfiguration - wird verwendet, um URLs mit Ansichten zu verknüpfen

urlpatterns = [
    path('products', ProductViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('products/<str:pk>', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('user', UserAPIView.as_view())
]
