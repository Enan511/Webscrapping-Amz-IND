# urls.py
from django.urls import path
from product.views import amazon_product_view

urlpatterns = [
    path('', amazon_product_view, name='amazon_product'),
]
