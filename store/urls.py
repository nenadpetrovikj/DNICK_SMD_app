from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('collections/<slug:category_slug>/', views.category_list, name='category_list'),
    path('add-product/', views.add_product, name='add_product'),
]
