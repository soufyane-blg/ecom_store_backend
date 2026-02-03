from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem, Order, OrderItem
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
# Create your views here.

def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "store/product_list.html", {
        "products": products
    })

def product_detail(request, slug):
    product= get_object_or_404(Product, slug= slug, is_active= True )
    return render (request, 'store/product_detail.html', {'product' : product})



from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def add_to_cart(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)

    
    if product.stock <= 0:
        messages.error(request, "This product is out of stock")
        return redirect("product_detail", slug=product.slug)

   
    if not request.user.is_authenticated:
        return redirect("login")

    
    cart, created = Cart.objects.get_or_create(user=request.user)

    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1

    cart_item.save()

    return redirect("product_list")

def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    return render(request, "store/cart_detail.html", {
        "cart": cart,
        "items": items
    })



def create_order(request):
    cart = Cart.objects.get(user=request.user)
    order = Order.objects.create(user=request.user)

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    cart.items.all().delete()

    messages.success(request, "Your order has been placed successfully")

    return redirect("thank_you", order_id=order.id)



def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("product_list")

    return render(request, "store/login.html")





def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            User.objects.create_user(username=username, password=password)
            return redirect("login")
        except IntegrityError:
            return render(request, "store/signup.html", {
                "error": "Username already exists"
            })

    return render(request, "store/signup.html")

def thank_you(request, order_id):
    if not request.user.is_authenticated:
        return redirect("login")
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, "store/thank_you.html", {"order": order})

def my_orders(request):
    if not request.user.is_authenticated:
        return redirect("login")
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "store/my_orders.html", {"orders": orders})