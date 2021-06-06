from django.contrib import admin
from django.urls import path,include
from .views import *
from . import views 

app_name="Tech_Parts"
urlpatterns = [
    path('',views.home,name="home" ),
    path("category/",views.category,name="category"),
    path("category/processor/",views.processor,name="processor"),
    path("category/processor/product/",views.product,name="product"),
    path("product-add/<str:slug>/",views.add_product,name="product_add"),
   
]
     