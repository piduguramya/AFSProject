from rest_framework import serializers
from .models import (Categories,
                        Products,
                        Product_item,
                        Variation,
                        Variation_option,
                        Product_Configuration,
                        ShoppingCart,
                        ShoppingCartItems,
                        Order,
                        Order_items,
                        AccountDeposit)

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields=["id","category","product_name","decription"]


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categories
        fields=["id","category_name"]


class Product_itemserializer(serializers.ModelSerializer):
    class Meta:
        model=Product_item
        fields='__all__'

class Product_itemserializerwithoutmrp(serializers.ModelSerializer):
    class Meta:
        model=Product_item
        fields=["id","product","sku","qty_in_stock","product_img","selling_price","description"]

class Variationserializer(serializers.ModelSerializer):
    class Meta:
        model=Variation
        fields='__all__'

class Variation_optionserializer(serializers.ModelSerializer):
    class Meta:
        model=Variation_option
        fields='__all__'

class Product_ConfigurationSerializer(serializers.ModelSerializer):
    # product_item=Product_item1serializer()
    variationoption=Variation_optionserializer()

    class Meta:
        model=Product_Configuration
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

class AccountDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model=AccountDeposit
        fields='__all__'


# <------------------## extra serializers ##----------------------------->
class categorywiseproducts(serializers.ModelSerializer):             ####extraaaaaaaaaaaaaaaaaaa serializer
    prods=ProductsSerializer(many=True,read_only=True)

    class Meta:
        model=Categories
        fields=["id","category_name","prods"]

class ProductsforitemsSerializer(serializers.ModelSerializer):
    prod_items=Product_itemserializer(many=True,read_only=True)

    class Meta:
        model=Products                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        fields=["category","product_name","decription","prod_items"]














