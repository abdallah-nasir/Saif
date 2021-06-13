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
    path("result/",views.result,name="result"),
    path("order/edit/<slug:slug>/",views.order_edit,name="order_edit"),    

    path("confirm/",views.confirm,name="confirm"),

    path("dashboard/",views.dashboard,name="dashboard"),
    path("dashboard/add/",views.add,name="add"),
    path("dashboard/edit/<str:slug>/",views.edit,name="edit"),
    path("dashboard/delete/<str:slug>/",views.delete,name="delete"),
    path("profile/",views.profile,name="profile"),
    path("team/",views.team,name="team"),

    path("dashboard/supplier/",views.supplier,name="supplier"),
     
]
     