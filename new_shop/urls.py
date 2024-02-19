from django.urls import path
from . import views

urlpatterns = [


    path('', views.index, name='index'),
    path('add_cart/<int:pr_id>', views.add_cart, name='add_cart'),
    path('add_quantity/<int:item_id>', views.add_quantity, name='add_quantity'),
    path('deduct_quantity/<int:item_id>',
         views.deduct_quantity, name='deduct_quantity'),
    path('delete_item/<int:item_id>',
         views.delete_item, name='delete_item'),
    path('cart', views.cart, name='cart'),
    path('search', views.search, name='search'),
    path('upload_products', views.upload_products, name="upload_products"),
    path('update_products/<int:pr_id>',
         views.update_products, name="update_products"),
    path('delete_products/<int:pr_id>',
         views.delete_products, name="delete_products"),
    path('product_details/<int:pr_id>',
         views.product_details, name="product_details"),
    path('category/<int:cat_id>',
         views.category, name="category"),
     path('admin_manage',
         views.admin_manage, name="admin_manage")
]
