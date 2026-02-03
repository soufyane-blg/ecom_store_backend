from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("checkout/", views.create_order, name="create_order"),
    path("login/", views.user_login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("thank-you/<int:order_id>/", views.thank_you, name="thank_you"),
    path("my-orders/", views.my_orders, name="my_orders"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)