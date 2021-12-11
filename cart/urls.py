from django.urls import path
from . import views

#cart urls
urlpatterns = [
    path('add_to_cart/<product_id>', views.add_to_cart, name="add_to_cart"),
    path('update_cart/', views.update_cart, name="update_cart"),
    path('cart/',views.cart,name='cart'),
    path('check_out/',views.check_out,name='check_out'),
]

