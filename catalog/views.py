from django.shortcuts import render
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
from account.models import UserAccount,Account                      
from .serializers import (CategoriesSerializer,
                            ProductsSerializer,
                            Product_itemserializer,
                            Variationserializer,
                            Variation_optionserializer,
                            Product_ConfigurationSerializer,
                            categorywiseproducts,
                            ProductsforitemsSerializer,
                            ShoppingCartSerializer,
                            ShoppingCartItemsSerializer,
                            OrderSerializer,
                            Order_itemsSerializer,
                            AccountDepositSerializer,
                            Product_itemserializerwithoutmrp)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAuthenticated



# Create your views here.
class CategoryprodsView(APIView):
    def get(self,request):
        queryset=Categories.objects.all()
        cpdata=categorywiseproducts(queryset,many=True).data
        
        return Response(cpdata)


class prodidView(APIView):
    def get(self,request,pk=None):
        queryset=Products.objects.get(id=pk)
        proddata=ProductsSerializer(queryset).data

        return Response(proddata)

class variantsView(APIView):
    def get(self,request):
        queryset=Categories.objects.all()
        categories=CategoriesSerializer(queryset,many=True,read_only=True).data

        for category in categories:
            print(category)
            variation=Variation.objects.filter(category__id=category["id"])
            variantsdata=Variationserializer(variation,many=True).data
            category["variants"]=variantsdata

            for variant in variantsdata:
                variant_id = variant["id"]
                options = Variation_option.objects.filter(variation__id=variant_id)
                variant["options"] = Variation_optionserializer(options, many=True).data

        return Response(categories)


class porductswithvariants(APIView):      #full view
    permission_classes=[IsAuthenticated]

    def get(self,request):
        queryset=Products.objects.all()
        products_data=ProductsSerializer(queryset,many=True).data

        for product in products_data:
            produtitem_query=Product_item.objects.filter(product__id=product["id"])
            product_items_data=Product_itemserializer(produtitem_query,many=True).data
            product["product_items"]=product_items_data

            for product_item in product_items_data:
                productvariant_query=Product_Configuration.objects.filter(product_item__id=product_item["id"])
                productvariant_data=Product_ConfigurationSerializer(productvariant_query,many=True).data
                product_item["productvariants"]=productvariant_data

        return Response(products_data)

class porductswithvariantstouser(APIView):      #full view
    
    def get(self,request):
        queryset=Products.objects.all()
        products_data=ProductsSerializer(queryset,many=True).data

        for product in products_data:
            produtitem_query=Product_item.objects.filter(product__id=product["id"])
            product_items_data=Product_itemserializerwithoutmrp(produtitem_query,many=True).data
            product["product_items"]=product_items_data

            for product_item in product_items_data:
                productvariant_query=Product_Configuration.objects.filter(product_item__id=product_item["id"])
                productvariant_data=Product_ConfigurationSerializer(productvariant_query,many=True).data
                product_item["productvariants"]=productvariant_data

        return Response(products_data)


class ProductsPriceOrder(APIView):
    def get(self,request):
        order=request.query_params.get("order","asc")

        # queryset=Products.objects.all()
        # products_data=ProductsforitemsSerializer(queryset,many=True).data

        # return Response(products_data)

# <------------------------another process---------------->

        queryset=Products.objects.all()
        products_data=ProductsSerializer(queryset,many=True).data

        for product in products_data:
            if order=="asc" or order=="ASC":
                product["items_in_order"]=Product_itemserializer(Product_item.objects.all().order_by("selling_price"),many=True).data
            elif order=="desc" or order=="DESC":
                product["items_in_order"]=Product_itemserializer(Product_item.objects.all().order_by("-selling_price"),many=True).data

        return Response(products_data)


class AddCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        addcategory=CategoriesSerializer(data=request.data)

        if addcategory.is_valid():
            try:
                addcategory.save()
                return Response({"category added successfully"},status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(str(e),status=status.HTTP_409_CONFLICT)
        else:
            return Response({"invalid json provided"},status=status.HTTP_400_BAD_REQUEST)

class AddProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        addproduct=ProductsSerializer(data=request.data)


        if addproduct.is_valid():
            try:
                addproduct.save()
                return Response({"product added successfully"},status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(str(e),status=status.HTTP_409_CONFLICT)
        else:
            return Response({"msg":"invalid json provided",
                               "error":addproduct.errors},status=status.HTTP_400_BAD_REQUEST)


class AddProductItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        addproductitem=Product_itemserializer(data=request.data)

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
        phone = request.data.get("phone_number")
        product_id = request.data.get("product_item")
        qty = int(request.data.get("qty", 1))

        if not phone or not product_id:
            return Response({"error": "Phone number and product ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Try to get the user
        user_qs = Account.objects.filter(phone_number=phone)
        if user_qs.exists():
            user = user_qs.first()
            print("user with that mbl number is present")
        else:
            user = Account.objects.create(phone_number=phone, name="xyz")
            user.save()
            user.refresh_from_db()
            print("user createdddddddddddddddd", user.id)


        # Try to get product
        try:
            product = Product_item.objects.get(id=product_id)
            print("product found")
        except Product_item.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        if product.qty_in_stock < qty:
            return Response({"error": "Not enough stock available"}, status=status.HTTP_400_BAD_REQUEST)

        print("started")
        # Get or create cart for the user
        try:
            cart, _ = ShoppingCart.objects.get_or_create(user=user)
        except Exception as e:
            print("Cart creation failed:", e)
            return Response({"error": str(e)}, status=500)

        print("created cart on the user or cart present")
        print("stopped")
        # Get or create cart item
        item, created = ShoppingCartItems.objects.get_or_create(
            cart_id=cart,    ####may be error
            product_item=product,
            defaults={
                'qty': qty,
                'sp': product.selling_price,
                'mrp': product.mrp,
            }
        )

        if not created:
            new_total_qty = item.qty + qty
            if product.qty_in_stock < new_total_qty:
                return Response({"error": "Not enough stock available for the requested quantity"}, status=status.HTTP_400_BAD_REQUEST)

            item.qty = new_total_qty
            item.save()

        serializer = ShoppingCartItemsSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateCartItemView(APIView):    #{qty: }
    def patch(self, request, item_id):
        try:
            item = ShoppingCartItems.objects.get(id=item_id)
        except ShoppingCartItems.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

        qty_delta = request.data.get("qty")
        if qty_delta is None:
            return Response({"error": "Quantity change required"}, status=400)

        try:
            qty_delta = int(qty_delta)
        except ValueError:
            return Response({"error": "Invalid quantity"}, status=400)

        # Calculate new quantity
        new_qty = item.qty + qty_delta

        if new_qty < 1:
            return Response({"error": "Quantity cannot be less than 1"}, status=400)

        if item.product_item.qty_in_stock < new_qty:
            return Response(
                {"error": f"Not enough stock for {item.product_item.sku}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        item.qty = new_qty

        # Use unit prices from product to update totals
        unit_sp = item.product_item.selling_price
        unit_mrp = item.product_item.mrp

        item.sp = unit_sp * new_qty
        item.mrp = unit_mrp * new_qty

        item.save()

        serializer = ShoppingCartItemsSerializer(item)
        return Response(serializer.data)


class DeleteCartItemView(APIView):
    def delete(self, request, item_id):
        try:
            item = ShoppingCartItems.objects.get(id=item_id)
        except ShoppingCartItems.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

        item.delete()
        return Response({"message": "Item deleted"}, status=204)
            

# -------orders--------------------#
class PlaceOrderView(APIView):
    def post(self, request):
        cart_id = request.data.get("cart_id")

        if not cart_id:
            return Response({"error": "Cart ID is required."}, status=400)

        try:
            cart = ShoppingCart.objects.get(cart_id=cart_id)
            cart_items = ShoppingCartItems.objects.filter(cart_id=cart)
        except ShoppingCart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=404)

        if not cart_items.exists():
            return Response({"error": "Cart is empty."}, status=400)

        total_sp = 0
        total_mrp = 0

        # Stock check
        for item in cart_items:
            if item.product_item.qty_in_stock < item.qty:
                return Response(
                    {"error": f"Not enough stock for {item.product_item.sku}"},
                    status=400
                )

        with transaction.atomic():
            # Create order
            order = Order.objects.create(
                user=cart.user,
                total_sp=0,  # Temporary
                total_mrp=0,
                payment=True  # You can replace this with real payment logic later
            )

            for item in cart_items:
                # Create order item
                Order_items.objects.create(
                    order=order,
                    items=item.product_item,
                    qty=item.qty,
                    sp=item.sp,
                    mrp=item.mrp
                )

                # Update totals
                total_sp += item.sp
                total_mrp += item.mrp

                # Reduce stock
                item.product_item.qty_in_stock -= item.qty
                item.product_item.save()

            # Update order totals
            order.total_sp = total_sp
            order.total_mrp = total_mrp
            order.save()

            # Clear the cart
            cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=201)

class UserOrdersView(APIView):
    def get(self, request,id):
        orders = Order.objects.filter(user_id__id=id)
        serializer = OrderSerializer(orders, many=True).data
        return Response(serializer)

class OrderItemsView(APIView):
    def get(self,request, order_id):
        order_items=Order_items.objects.filter(order__id=order_id)
        serializer=Order_itemsSerializer(order_items,many=True).data
        return Response(serializer)



class AddAccountDeposits(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        depositsdata=AccountDepositSerializer(data=request.data)

        if depositsdata.is_valid():
            try:
                depositsdata.save()
                return Response("data added successfully",status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(str(e),status=status.HTTP_409_CONFLICT)
        else:
            return Response("invalid json",status=status.HTTP_400_BAD_REQUEST)


