
from django.urls import path
from .views.home import home
from .views.signup import signup
from .views.login import login, logout
from .views.products import product_detail
from .views.cart import cart, add_to_cart, update_cart, remove_from_cart
from .views.checkout import checkout, order_detail, order_list
from .views.api import api_categories, api_product_detail, api_products
#
urlpatterns = [
    path("", home.as_view(), name="home"),
    path("product/<int:product_id>/", product_detail, name="product_detail"),
    path("api/categories/", api_categories, name="api_categories"),
    path("api/products/", api_products, name="api_products"),
    path("api/products/<int:product_id>/", api_product_detail, name="api_product_detail"),
    path('signup/', signup.as_view(), name='signup'),
    path('login/', login.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('cart/', cart, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/', update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_list, name='orders'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
]
