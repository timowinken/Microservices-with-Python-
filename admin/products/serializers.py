from rest_framework import serializers

from .models import Product

#Werkzeug, das es ermöglich Django-Modelle in JSON-Daten umzuwandeln
class ProductSerializer(serializers.ModelSerializer):
    #Instanzen des Product-Models werden in serialisierte Daten umgewandelt und umgekehrt
    class Meta:
        model = Product
        fields = '__all__' #Alle Felder serialisieren