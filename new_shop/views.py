from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegistrationForm
from .forms import ProductForm, AddCartForm, CategoryForm
from .models import Product, AddCart, Category, CategoryProduct
from django.db.models import Count, Sum, Q
from django.contrib.auth.models import User, AnonymousUser
from PIL import Image
from django.http import HttpResponseRedirect

def index(request):
    all_products = Product.product_objects.all()
    all_categories = Category.category_objects.all()
    form = AddCartForm(request.POST)

    num_items_cart = 0

    user = request.user
    my_cart = AddCart.cart_objects.all().order_by('-id')
    my_cart = my_cart.filter(client=user)
    for item in my_cart:
        num_items_cart += item.quantity

    return render(request, 'index.html', {'form': form, 'all_products': all_products, 'num_items_cart': num_items_cart, 'all_categories': all_categories})

def category(request, cat_id):
    this_category = Category.category_objects.get(id=cat_id)
    cat_products = Product.product_objects.filter(category_id=cat_id)
    all_products = Product.product_objects.all()
    all_categories = Category.category_objects.all()
    form = AddCartForm(request.POST)

    return render(request, 'category.html', {'cat_products': cat_products, 'this_category': this_category, 'form': form, 'all_products': all_products, 'all_categories': all_categories})

def search(request):
    form = AddCartForm(request.POST)
    all_categories = Category.category_objects.all()
    form_add = AddCartForm()
    all_products = Product.product_objects.all()
    search = ''
    search_results = []

    if request.method == "POST":
        search = request.POST['search'].lower()
        if search:
            search_results = Product.product_objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search))
            request.session['last_search'] = search
        else: 
            search = request.session.get('last_search')

    return render(request, 'search_results.html', {'all_categories': all_categories, 'search': search, 'form_add': form_add, 'search_results': search_results, 'all_products': all_products, 'form': form})


def add_cart(request, pr_id):
    this_product = Product.product_objects.get(id=pr_id)
    if request.method == "POST":
        client = request.user
        all_in_cart = AddCart.cart_objects.filter(client=client)
        form = AddCartForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            for item in all_in_cart:
                if item.product_id.id == this_product.id:
                    x = f.quantity
                    item.add_quantity(x)
                    item.save()
                    this_product.calc_clicks = this_product.calc_clicks + 1
                    this_product.save() 
                    print(this_product.name, this_product.calc_clicks)
                    return redirect('cart')
            f.product_id = this_product
            f.client = client
            f.save()
            this_product.calc_clicks = 1
            this_product.save()
            print(this_product.name, this_product.calc_clicks)
            return redirect('cart')

    return render(request, 'index.html', {'form': form, 'this_product': this_product, })


def cart(request):
    all_categories = Category.category_objects.all()

    total_to_pay = 0

    my_cart = AddCart.cart_objects.all().order_by('-id')

    client = request.user
    my_cart = my_cart.filter(client=client)

    for item in my_cart:
        if item.product_id.on_sale > 0:
            total_per_item = item.discounted_price()
            total_to_pay = total_to_pay + total_per_item
        else:
            total_per_item = item.total_price_per_item()
            total_to_pay = total_to_pay + total_per_item

    return render(request, 'cart.html', {'all_categories': all_categories,  'my_cart': my_cart, 'total_to_pay': total_to_pay})


def add_quantity(request, item_id):
    this_order = AddCart.cart_objects.get(id=item_id)
    if this_order is not None:
        this_order.quantity = this_order.add_quantity(1)
        this_order.total_price = this_order.total_price_per_item()
        this_order.save()
        return redirect('cart')

    return render(request, 'cart.html', {'this_order': this_order, })


def deduct_quantity(request, item_id):
    this_order = AddCart.cart_objects.get(id=item_id)
    if this_order is not None:
        this_order.quantity = this_order.deduct_quantity()
        this_order.total_price = this_order.total_price_per_item()
        this_order.save()
        if this_order.quantity <= 0:
            this_order.delete()
        return redirect('cart')

    return render(request, 'cart.html', {'this_order': this_order})


def delete_item(request, item_id):
    this_item = AddCart.cart_objects.get(id=item_id)
    if this_item is not None:
        this_item.delete()
        return redirect('cart')

    return render(request, 'cart.html', {'this_item': this_item})


def product_details(request, pr_id):
    all_categories = Category.category_objects.all()
    this_product = Product.product_objects.get(id=pr_id)
    all_products = Product.product_objects.all()
    form = AddCartForm(request.POST)

    if this_product.on_sale > 0:
        my_discount = this_product.price - (this_product.price * this_product.on_sale / 100)
    else:
        my_discount = 0
   
    return render(request, 'product_details.html', {'all_categories': all_categories,  'this_product': this_product, 'all_products': all_products, 'form': form, 'my_discount': my_discount, })


def upload_products(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_manage')
    else:
        form = ProductForm()

    return render(request, 'upload_products.html', {'form': form, })


def update_products(request, pr_id):
    this_product = Product.product_objects.get(id=pr_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=this_product)
        if form.is_valid():
            form.save()
            return redirect('admin_manage')
    else: 
        form = ProductForm(instance=this_product)

    return render(request, 'update_products.html', {'form': form,  'this_product': this_product})


def delete_products(request, pr_id):
    this_product = Product.product_objects.get(id=pr_id)
    this_product.delete()
    return redirect('admin_manage')

    
def admin_manage(request):
    all_products = Product.product_objects.all()

    return render (request, 'admin_manage_store.html', {'all_products': all_products})


