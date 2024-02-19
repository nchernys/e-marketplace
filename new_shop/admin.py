from django.contrib import admin
from .models import Product, AddCart, Category

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(AddCart)



# Register your models here.
