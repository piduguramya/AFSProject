from django.contrib import admin
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

# Register your models here.
admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Product_item)
admin.site.register(Variation)
admin.site.register(Variation_option)
admin.site.register(Product_Configuration)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItems)
admin.site.register(Order)
admin.site.register(Order_items)
admin.site.register(AccountDeposit)


