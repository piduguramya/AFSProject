from django.urls import path 
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns=[
    path("prods/",views.CategoryprodsView.as_view()),
    path("prodwithid/<int:pk>",views.prodidView.as_view()),
    path("variants/",views.variantsView.as_view()),
    path("full/",views.porductswithvariants.as_view()),
    path('order/',  views.ProductsPriceOrder.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),



]