from django.db import models
from django.forms import ModelForm
from django import forms
from .models import Category

from .models import Product, AddCart,  CategoryProduct

list_of_categories = [("music", "music")]

cat_choices = Category.category_objects.all()
if cat_choices: 
    for obj in cat_choices:
        list_of_categories.append((obj.name, obj.name))

class CategoryForm(ModelForm):
    class Meta:
        model = Category

        fields = ['name',]
        labels = {
        }

        widgets = {
            'category': forms.Select(choices=list_of_categories, attrs={'class': 'form-control form-control', }),
        }

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category_id',
                  'price', 'on_sale', 'image', ]
        labels = {
            "category_id": "Category"
        }

        categories = forms.ModelMultipleChoiceField(
            queryset=Category.category_objects.all(),
        )

        widgets = {
            'on_sale': forms.Select(attrs={'class': 'form-control form-control', }),
            'category_id': forms.CheckboxSelectMultiple(attrs={'class': 'form-control form-control', })
        }

choices = [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"),
           ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10")]


class AddCartForm(ModelForm):
    class Meta:
        model = AddCart
        fields = ['quantity']
        labels = {

        }

        widgets = {
            "quantity": forms.Select(choices=choices, attrs={'class': 'form-control form-control-sm', }),
        }

