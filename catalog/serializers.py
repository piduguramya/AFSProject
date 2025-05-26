from .models import Categories,Products,GenderCategory,Catelog
from rest_framework import serializers

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categories
        fields=["id","category_name"]

class ProductsSerializers(serializers.ModelSerializer):
    class  Meta:
        model=Products
        fields='__all__'

class GenderCategorySerializers(serializers.ModelSerializer):
    Category=CategoriesSerializer()

    class Meta:
        model=GenderCategory
        fields=['categorytype_name',"Category"]


class CatelogSerializers(serializers.ModelSerializer):
    product_id=ProductsSerializers()

    class Meta:
        model=Catelog
        fields=["categorytype_name","catelog_name","product_id"]














