from django.contrib import admin
from django.urls import path,include
from .views import *
from . import views 

app_name="Tech_Parts"
urlpatterns = [
    path('',views.home,name="home" ),       
    path("category/",views.category,name="category"),   
    path("category/processor/",views.processor,name="processor"),
    # path("category/processor/product/",views.product,name="product"),
    
    path("category/processor/processor-products/",views.processor_filter,name="processor_filter"),
    path("category/processor/gpu-products/",views.gpu_filter,name="gpu_filter"),
    path("category/processor/motherboard-products/",views.motherboard_filter,name="motherboard_filter"),
    path("category/processor/ram-products/",views.ram_filter,name="ram_filter"),
    path("category/processor/hard-products/",views.hard_filter,name="hard_filter"),
    path("category/processor/cooler-products/",views.cooler_filter,name="cooler_filter"),
    path("category/processor/powersupply-products/",views.powersupply_filter,name="powersupply_filter"),

    path("result/",views.result,name="result"),    
    path("suppliers/",views.supplier,name="suppliers"),
    path("suppliers/<str:id>/",views.edit_supplier,name="edit_supplier"),
    path("dashboard/supplier/",views.add_supplier,name="add_supplier"),

    path("add-similar/<str:id>/",views.add_similar_product,name="add-similar"),
    path("remove-similar/<str:id>/",views.remove_similar_product,name="remove-similar"),
   
    path("order/edit/<slug:slug>/",views.order_edit,name="order_edit"),    
    path("cart/edit/<slug:slug>/",views.cart_edit,name="cart_edit"),    

    path("confirm/",views.confirm,name="confirm"),

    path("dashboard/",views.dashboard,name="dashboard"),
    path("dashboard/add/",views.add,name="add"),
    path("dashboard/edit/<str:slug>/",views.edit,name="edit"),
    path("dashboard/delete/<str:slug>/",views.delete,name="delete"),
    path("games/",views.gammes,name="gammes"),
    path("games/<str:slug>/edit/",views.gammes_edit,name="gammes_edit"),
    path("fps/",views.fps,name="fps"),
    path("fps/add/",views.fps_add,name="fps_add"),

    path("fps/<str:id>/",views.fps_edit,name="fps_edit"),

    path("profile/",views.profile,name="profile"),
    path("team/",views.team,name="team"),

     
]
     