from django.urls import path
from . import views



urlpatterns = [
    path('', views.home_page, name="home"),
    path('search/',views.search, name="search"),
    path('product/<product_id>', views.product_detail, name='product_details'),
    path('category/<category_name>', views.category_list, name='category_list'),
]

