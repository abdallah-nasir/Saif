from django.contrib import admin
from .models import *
# Register your models here.
class Admin(admin.ModelAdmin):
    list_display=["customer","device"]
class Ordered(admin.ModelAdmin):
    list_display=["customer","ordered","device"]
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Product)
# admin.site.register(Account)
admin.site.register(Order,Ordered)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Processor)
admin.site.register(Filters,Admin) 
admin.site.register(Gammes)   