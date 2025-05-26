from django.db import models


# Create your models here.
class Categories(models.Model):
    category_name=models.CharField(max_length=255)  # clothings / acessaries / electronics /home &furnitures /Grocery & essentials

    def __str__(self):
        return self.category_name


class Products(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=255)
    cost_price=models.DecimalField(decimal_places=2, max_digits=10)
    discount=models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    selling_price=models.DecimalField(decimal_places=2, max_digits=10)
    decription=models.CharField(max_length=500)
    product_weight=models.DecimalField(decimal_places=2, max_digits=5)
    product_color=models.CharField(max_length=255)
    stock=models.BooleanField(default=True)


    def save(self, *args, **Kwargs):
        discountprice = self.cost_price*(1-(self.discount/100))
         
        if discountprice < self.selling_price and discountprice > 0:
            self.selling_price =discountprice
        else:
            self.selling_price=self.cost_price
        super().save(*args, **Kwargs)

    def __str__(self):
        return self.product_name


class GenderCategory(models.Model): #id primary
    categorytype_name=models.CharField(max_length=255)  #Men / Women / Mobiles / Laptops / Accessories /Bedroom / Kitchen / Decor / Lighting / Beverages / Snacks / Fresh Produce / Household
    Category=models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="Category")

    def __str__(self):
        return self.categorytype_name


class Catelog(models.Model):
    categorytype_name=models.CharField(max_length=255)  #Men / Women / Mobiles / Laptops / Accessories /Bedroom / Kitchen / Decor / Lighting / Beverages / Snacks / Fresh Produce / Household
    catelog_name=models.CharField(max_length=225, null=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.catelog_name


# <------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>
   








     




    
