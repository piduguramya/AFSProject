from rest_framework import serializers
from .models import (Categories1,
                        Products1,
                        Product_item1,
                        Variation1,
                        Variation_option1,
                        Product_Configuration1,
                        ShoppingCart,
                        ShoppingCartItems,
                        Order,
                        Order_items)

class Products1Serializer(serializers.ModelSerializer):
    class Meta:
        model=Products1
        fields=["id","category","product_name","decription"]


class Categories1Serializer(serializers.ModelSerializer):

    class Meta:
        model=Categories1
        fields=["id","category_name"]


class Product_item1serializer(serializers.ModelSerializer):
    class Meta:
        model=Product_item1
        fields='__all__'

class Variation1serializer(serializers.ModelSerializer):
    class Meta:
        model=Variation1
        fields='__all__'

class Variation_option1serializer(serializers.ModelSerializer):
    class Meta:
        model=Variation_option1
        fields='__all__'

class Product_Configuration1Serializer(serializers.ModelSerializer):
    # product_item=Product_item1serializer()
    variationoption=Variation_option1serializer()

    class Meta:
        model=Product_Configuration1
        fields=["product_item","variationoption"]


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShoppingCart
        fields="__all__"

class ShoppingCartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShoppingCartItems
        fields="__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"

class Order_itemsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order_items
        fields="__all__"



# <------------------## extra serializers ##----------------------------->



class categorywiseproducts(serializers.ModelSerializer):             ####extraaaaaaaaaaaaaaaaaaa serializer
    prods=Products1Serializer(many=True,read_only=True)

    class Meta:
        model=Categories1
        fields=["id","category_name","prods"]

class Products1foritemsSerializer(serializers.ModelSerializer):
    prod_items=Product_item1serializer(many=True,read_only=True)

    class Meta:
        model=Products1
        fields=["category","product_name","decription","prod_items"]















