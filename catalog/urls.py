from django.urls import path 
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Product-related views
    path("prods/", views.CategoryprodsView.as_view()),
    path("prodwithid/<int:pk>", views.prodidView.as_view()),
    path("variants/", views.variantsView.as_view()),
    path("full/", views.porductswithvariants.as_view()),
    path("priceorder/", views.ProductsPriceOrder.as_view()),

    # Add category, product, and product item
    path("add-category/", views.AddCategoryView.as_view()),
    path("add-product/", views.AddProductView.as_view()),
    path("add-product-item/", views.AddProductItemView.as_view()),

    # Cart endpoints
    path("cart/add/", views.AddToCartView.as_view()),
    path("cart/update/<int:item_id>/", views.UpdateCartItemView.as_view()),
    path("cart/delete/<int:item_id>/", views.DeleteCartItemView.as_view()),

    # Order endpoints
    path("place-order/", views.PlaceOrderView.as_view()),
    path("userorders/<int:id>/", views.UserOrdersView.as_view()),

    # Order_items endpoints
    path("order_items/<int:order_id>/",views.OrderItemsView.as_view()),

    # AccountDeposit endpoints
    path("deposits/",views.AddAccountDeposits.as_view()),

    # JWT Auth
    path("api/token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
]


