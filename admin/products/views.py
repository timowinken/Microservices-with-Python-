from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, User
#from .producer import publish
from .serializers import ProductSerializer
import random

# Create your views here.

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):    
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data) 

    def create(self, request):  
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None): 
        pass

    def update(self, request, pk=None):   
        pass

    def destroy(self, request, pk=None):  
        pass