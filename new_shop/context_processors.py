from .models import AddCart 

def common_data(request):
    
    user = request.user
    num_items_cart = 0

    my_cart = AddCart.cart_objects.filter(client=user).order_by('-id')
    for item in my_cart:
        num_items_cart += item.quantity

    return {'num_items_cart': num_items_cart}