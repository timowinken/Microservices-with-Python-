from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, User
from .producer import publish
from .serializers import ProductSerializer
import random


# Django-Views - Verarbeitung von HTTP-Anfragen und -Antworten

class ProductViewSet(viewsets.ViewSet): #Methoden, die aufgerufen werden, wenn Anfrage an bestimmte URL gesendet wird

    #GET-Anfrage: gibt Liste aller Produkte zurück
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    #POST-Anfrage: erstellt ein neues Produkt aus übergebenen Daten
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    #GET-Anfrage: URL mit bestimmter Produkt-ID gibt angegebenes Produkt zurück
    def retrieve(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    #PUT-Anfrage: URL mit bestimmter Produkt-ID aktualisiert angegebenes Produkt
    def update(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    #DELETE-Anfrage: URL mit bestimmter Produkt-ID löscht angegebenes Produkt
    def destroy(self, request, pk=None):
        product = Product.objects.get(id=pk)
        product.delete()
        publish('product_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):

    #GET-Anfrage: Wählt zufälligen Benutzer aus der Datenbank aus und gibt ihn in einer Antwort zurück
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id': user.id
        })
