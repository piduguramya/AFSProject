from django.contrib import admin
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

# Register your models here.
admin.site.register(Categories1)
admin.site.register(Products1)
admin.site.register(Product_item1)
admin.site.register(Variation1)
admin.site.register(Variation_option1)
admin.site.register(Product_Configuration1)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItems)
admin.site.register(Order)
admin.site.register(Order_items)


