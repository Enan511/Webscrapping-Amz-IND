from django.contrib import admin
from django.urls import path
from product import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.upload_csv, name='upload_csv'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
