from django.contrib import admin
from .models import Products, Categories, GenderCategory,Catelog

# Register your models here.

admin.site.register(Categories)
admin.site.register(GenderCategory)
admin.site.register(Products)
admin.site.register(Catelog)
