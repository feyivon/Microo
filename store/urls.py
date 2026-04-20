from django.urls import path
from .views import shop, product_detail, Cart, add_to_cart, remove_from_cart, remove_cart_item, cart, checkout, order_complete, track_order, my_orders

urlpatterns = [
    path('shop/', shop, name= 'shop'),
    path('shop/<slug:category_slug>/', shop, name='products_by_category'),
    path('shop/<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),

    path('cart/', cart, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/remove-item/<int:product_id>/', remove_cart_item, name='remove_cart_item'),
    path('checkout/', checkout, name='checkout'),
    path('order/complete/<int:order_id>/', order_complete, name='order_complete'),
    path('order/track/', track_order, name='track_order'),       
    path('order/my-orders/', my_orders, name='my_orders'),   

]