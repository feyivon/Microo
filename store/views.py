from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from store.models import Product, Category, Cart, CartItem, Order, OrderItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

# Create your views here.
def shop(request, category_slug= None):
    categories = Category.objects.all()         
    selected_category = None
    products = Product.objects.filter(is_available = True)

    if category_slug:
        selected_category=get_object_or_404(Category, slug=category_slug)
        products = products.filter(category= selected_category)
    else:
        products = Product.objects.filter(is_available=True)
    product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
        'categories': categories,
        'selected_category': category_slug,
    }
    return render(request, 'shop.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_available=True)
    context = {
        'product': product,
    }
    return render(request, 'product_detail.html', context)


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
    return cart

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id = product_id)
    quantity = int(request.POST.get('quantity', 1))

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += quantity   # ← adds to existing quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=quantity
        )
        cart_item.save()

    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, cart_id = _cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def checkout(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        total = sum(item.product.price * item.quantity for item in cart_items)
        quantity = sum(item.quantity for item in cart_items)
    except ObjectDoesNotExist:
        return redirect('cart')

    if request.method == 'POST':
        full_name      = request.POST.get('full_name')
        email          = request.POST.get('email')
        phone_number   = request.POST.get('phone_number')
        address        = request.POST.get('address')
        city           = request.POST.get('city')
        state          = request.POST.get('state')
        country        = request.POST.get('country')
        payment_method = request.POST.get('payment_method')

        #Validate all fields filled
        if not all([full_name, email, phone_number, address, city, state, country]):
            messages.error(request, 'Please fill in all the fields.')
            return redirect('checkout')

        #Create the Order
        order = Order.objects.create(
            user           = request.user,
            full_name      = full_name,
            email          = email,
            phone_number   = phone_number,
            address        = address,
            city           = city,
            state          = state,
            country        = country,
            total          = total,
            payment_method = payment_method,
            is_ordered     = True,
        )

        #Save each cart item as an OrderItem
        for item in cart_items:
            OrderItem.objects.create(
                order    = order,
                product  = item.product,
                quantity = item.quantity,
                price    = item.product.price,
            )

            #Reduce stock after order
            item.product.stock -= item.quantity
            item.product.save()

        #Clear the cart after order
        cart_items.delete()

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_complete', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
    }
    return render(request, 'checkout.html', context)


def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order_complete.html', context)


@login_required(login_url='login')
def track_order(request):
    orders = None
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            orders = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            messages.error(request, 'No order found with that ID. Please check and try again.')
            return redirect('track_order')

    return render(request, 'track_order.html', {'orders': orders})



@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'my_order.html', context)

