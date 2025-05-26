from django.shortcuts import render
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
from account.models import UserAccount,Account                      
from .serializers import (Categories1Serializer,
                            Products1Serializer,
                            Product_item1serializer,
                            Variation1serializer,
                            Variation_option1serializer,
                            Product_Configuration1Serializer,
                            categorywiseproducts,
                            Products1foritemsSerializer,
                            ShoppingCartSerializer,
                            ShoppingCartItemsSerializer,
                            OrderSerializer,
                            Order_itemsSerializer
                            )
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status



# Create your views here.
class CategoryprodsView(APIView):
    def get(self,request):
        queryset=Categories1.objects.all()
        cpdata=categorywiseproducts(queryset,many=True).data

        return Response(cpdata)


class prodidView(APIView):
    def get(self,request,pk=None):
        queryset=Products1.objects.all()
        proddata=Products1Serializer(queryset).data

        return Response(proddata)

class variantsView(APIView):
    def get(self,request):
        queryset=Categories1.objects.all()
        categories=Categories1Serializer(queryset,many=True,read_only=True).data

        for category in categories:
            print(category)
            variation=Variation1.objects.filter(category__id=category["id"])
            variantsdata=Variation1serializer(variation,many=True).data
            category["variants"]=variantsdata

            for variant in variantsdata:
                query=Variation_option1.objects.all()
                variant["options"]=Variation_option1serializer(query,many=True,read_only=True).data

        return Response(categories)


class porductswithvariants(APIView):
    def get(self,request):
        queryset=Products1.objects.all()
        products_data=Products1Serializer(queryset,many=True).data

        for product in products_data:
            produtitem_query=Product_item1.objects.filter(product__id=product["id"])
            product_items_data=Product_item1serializer(produtitem_query,many=True).data
            product["product_items"]=product_items_data

            for product_item in product_items_data:
                productvariant_query=Product_Configuration1.objects.filter(product_item__id=product_item["id"])
                productvariant_data=Product_Configuration1Serializer(productvariant_query,many=True).data
                product_item["productvariants"]=productvariant_data

        return Response(products_data)

class ProductsPriceOrder(APIView):
    def get(self,request):
        order=request.query_params.get("order","asc")

        # queryset=Products1.objects.all()
        # products_data=Products1foritemsSerializer(queryset,many=True).data

        # return Response(products_data)

# <------------------------another process---------------->

        queryset=Products1.objects.all()
        products_data=Products1Serializer(queryset,many=True).data

        for product in products_data:
            if order=="asc" or order=="ASC":
                product["items_in_order"]=Product_item1serializer(Product_item1.objects.all().order_by("mrp"),many=True).data
            elif order=="desc" or order=="DESC":
                product["items_in_order"]=Product_item1serializer(Product_item1.objects.all().order_by("-mrp"),many=True).data

        return Response(products_data)


class AddCategoryView(APIView):
    def post(self,request):
        addcategory=Categories1Serializer(data=request.data)

        if addcategory.is_valid():
            try:
                addcategory.save()
                return Response({"category added successfully"},status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(str(e),status=status.HTTP_409_CONFLICT)
        else:
            return Response({"invalid json provided"},status=status.HTTP_400_BAD_REQUEST)

class AddProductView(APIView):
    def post(self,request):
        addproduct=Products1Serializer(data=request.data)

        if addproduct.is_valid():
            try:
                addproduct.save()
                return Response({"product added successfully"},status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(str(e),status=status.HTTP_409_CONFLICT)
        else:
            return Response({"invalid json provided"},status=status.HTTP_400_BAD_REQUEST)


class AddProductItemView(APIView):
    def post(self,request):
        addproductitem=Product_item1Serializer(data=request.data)

        if addproductitem.is_valid():
            try:
                addproductitem.save()
                return Response({"product_item added successfully"},status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(str(e),status=status.HTTP_409_CONFLICT)
        else:
            return Response({"invalid json provided"},status=status.HTTP_400_BAD_REQUEST)


###-------------cart logic------------------##
class AddToCartView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        product_id = request.data.get("product_item")
        qty = int(request.data.get("qty", 1))

        try:
            product = Product_item1.objects.get(id=product_id)
        except Product_item1.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        cart, _ = ShoppingCart.objects.get_or_create(user_id=user_id)

        item, created = ShoppingCartItems.objects.get_or_create(
            cart_id=cart,
            product_item=product,
            defaults={'qty': qty}
        )

        if not created:
            item.qty += qty

        item.save()

        serializer = ShoppingCartItemSerializer(item)
        return Response(serializer.data, status=201)

class UpdateCartItemView(APIView):
    def patch(self, request, item_id):
        try:
            item = ShoppingCartItems.objects.get(id=item_id)
        except ShoppingCartItems.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

        qty = request.data.get("qty")
        if qty:
            item.qty = int(qty)
            item.save()

        serializer = ShoppingCartItemSerializer(item)
        return Response(serializer.data)

class DeleteCartItemView(APIView):
    def delete(self, request, item_id):
        try:
            item = ShoppingCartItems.objects.get(id=item_id)
        except ShoppingCartItems.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

        item.delete()
        return Response({"message": "Item deleted"}, status=204)
            
















