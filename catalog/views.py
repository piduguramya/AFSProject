from django.shortcuts import render
from .models import Categories, Products,Catelog, GenderCategory
from .serializers import CategoriesSerializer, ProductsSerializers, CatelogSerializers, GenderCategorySerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

8
# Create your views here.
class AddCategoryView(APIView):
    def post(self,request):
        add_category=CategoriesSerializer(data=request.data)

        if add_category.is_valid():
            try:
                add_category.save()
                return Response({
                    "message":'category created successfully',
                    "data":add_category.data},
                    status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "message":str(e)},
                    status=status.HTTP_409_conflict)
        else:
            return Response({
                "message":create_user.errors},
                status=status.HTTP_400_BAD_REQUEST)

class AddProductView(APIView):
    def post(self,request):
        data=request.data

        is_bulk=isinstance(data,list)

        add_prod=ProductsSerializers(data=data, many=is_bulk)

        if add_prod.is_valid():
            try:
                add_prod.save()
                return Response({
                    "message":"product added sucessfully" if is_bulk else "product added sucessfully",
                    "data":add_prod.data},
                    status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "message":str(e)},
                    status=status.HTTP_409_CONFLICT)
        else:
            return Response(add_prod.errors,status=status.HTTP_400_BAD_REQUEST)

class DltcategoryView(APIView):
    def delete(self,request):
        data=request.data

        category_name=data.get("category_name")

        category=Categories.objects.get(category_name=category_name)

        if category:
            try:
                category.delete()
                return Response("cat deleteed sucessfully")
            except Exception as e:
                return Response(str(e))
        else:
            return Response("No such category present")


class DltProductView(APIView):
    def delete(self,request):
        data=request.data

        product_name=data.get("product_name")

        product=Products.objects.filter(product_name=product_name)

        if product:
            try:
                product.delete()
                return Response("product deleteed sucessfully")
            except Exception as e:
                return Response(str(e))
        else:
            return Response("No such product present")

class UpdateProductView(APIView):
    def patch(self,request):
        data=request.data
        product_name=data.get("product_name")
        product=Products.objects.get(product_name=product_name)

        if product:
            serilaizer=ProductsSerializers(product,data=data)
            if serilaizer.is_valid():
                try:
                    serilaizer.save()
                    return Response({"updated"})
                except Exception as e:
                    return Response(str(e))
            else:
                return Response({"invalild data"})
        else:
            return Response({"product name is mandatory"})

class RetrieveView(APIView):
    def get(self,request,pk=None):
        if pk:
            try:
                products=Products.objects.filter(Category__id=pk)
                serilaizer=ProductsSerializers(products,many=True)
                return Response(serilaizer.data)
            except Exception as e:
                return Response(str(e))
        else:
            products=Products.objects.all()
            serializer=ProductsSerializers(products,many=True)

            return Response(serializer.data)

class CatelogWiseData(APIView):
    def get(self,request):
        all_catelogs=Catelog.objects.all()
        data=CatelogSerializers(all_catelogs,many=True).data
        
        # for catelog in data:
        #     print(catelog)
        #     products=Products.objects.filter(product_id=catelog["product_id"])
        #     catelog["products"]=ProductsSerializers(products,many=True).data
             
        return Response(data)
            

class CategoryRelatedView(APIView):
    def get(self,request):
        queryset=Categories.objects.all()
        cat_ser=CategoriesSerializer(queryset,many=True).data

        for category in cat_ser:
            subcat=GenderCategory.objects.filter(Category__id=category["id"])
            subcat_ser=GenderCategorySerializers(subcat,many=True).data
            category["sub_category"]=subcat_ser

            for sub_category in subcat_ser:
                catelog=Catelog.objects.filter(categorytype_name=sub_category["categorytype_name"])
                data=CatelogSerializers(catelog,many=True).data
                sub_category["catelogs"]=data

        return Response(cat_ser)

        
# class CategoryWiseData(APIView):
#     def get(self,request):
#         all_cats=Categories.objects.all()
#         cats_data=CategoriesSerializer(all_cats,many=True).data

#         for category in cats_data:
#             products=Products.objects.filter(Category__id=category["id"])
#             category["products"]=ProductsSerializers(products,many=True).data
        
#         return Response(cats_data)
            





    

