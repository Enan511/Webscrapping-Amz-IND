# urls.py
from django.urls import path
from product.views import product_details_view

urlpatterns = [
    path('', product_details_view, name='amazon_product'),
]
