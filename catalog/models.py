from django.db import models
from account.models import UserAccount,Account

# Create your models here.
class Categories(models.Model):
    category_name=models.CharField(max_length=255)  # clothings / acessaries / electronics /home &furnitures /Grocery & essentials

    def __str__(self):
        return self.category_name


class Products(models.Model):
    category=models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="prods")
    product_name=models.CharField(max_length=255)
    decription=models.TextField()

    def __str__(self):
        return self.product_name


class Product_item(models.Model):
    product=models.ForeignKey(Products, on_delete=models.CASCADE, related_name="prod_items")
    sku=models.CharField(max_length=100)
    qty_in_stock=models.IntegerField()
    product_img=models.ImageField(upload_to="items/", blank=True)
    cp=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)     ### price retailaer bought 10rs
    mrp=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)    ### price  he should sell according to govt 20rs
    selling_price=models.DecimalField(max_digits=10, decimal_places=2)  ## price at which he sold 25rs
    description=models.TextField()

    def __str__(self):
        return self.sku

class  Variation(models.Model):
    category=models.ForeignKey(Categories, on_delete=models.CASCADE,related_name="categories")
    variation_name=models.CharField(max_length=100)

    def __str__(self):
        return self.variation_name

class Variation_option(models.Model):
    variation=models.ForeignKey(Variation, on_delete=models.CASCADE,related_name="variations")
    value=models.CharField(max_length=100)

    def __str__(self):
        return self.value

class Product_Configuration(models.Model):
    product_item=models.ForeignKey(Product_item, on_delete=models.CASCADE,related_name="product_items")
    variationoption=models.ForeignKey(Variation_option, on_delete=models.CASCADE,related_name="variation_options")

    def __str__(self):
        return f"{self.product_item.sku} and {self.variationoption.value}"

class ShoppingCart(models.Model):                     
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cart_id)


class ShoppingCartItems(models.Model):
    cart_id=models.ForeignKey(ShoppingCart, on_delete=models.CASCADE,related_name="cart_user")
    product_item=models.ForeignKey(Product_item, on_delete=models.CASCADE,related_name="cart_items")
    qty=models.PositiveIntegerField(default=1)
    sp=models.DecimalField(max_digits=10, decimal_places=2)
    mrp=models.DecimalField(max_digits=10, decimal_places=2)


    def save(self, *args, **Kwargs):
        self.sp=self.qty*self.product_item.selling_price
        self.mrp=self.qty*self.product_item.mrp
        super().save(*args, **Kwargs)


    def __str__(self):
        return self.product_item.sku

class Order(models.Model):   #order_id=auto
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    total_sp=models.DecimalField(max_digits=10, decimal_places=2)   # price sold  
    total_mrp=models.DecimalField(max_digits=10, decimal_places=2)    ##Price displayed
    payment=models.BooleanField()
    
    def __str__(self):
        return f"{self.user.name}s oder "

class Order_items(models.Model): # order_items_id is automatic
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    items=models.ForeignKey(Product_item, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    sp = models.DecimalField(max_digits=10, decimal_places=2)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"order items are of user {self.order.user.name} " 


class AccountDeposit(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    paid_on=models.DateTimeField(auto_now_add=True)
    desciption=models.TextField()
    
    def __str__(self):
        return f"{self.user.name}'s deposits"




