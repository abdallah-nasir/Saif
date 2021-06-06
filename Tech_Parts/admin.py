from django.contrib import admin
from .models import *
# Register your models here.
class Admin(admin.ModelAdmin):
    list_display=["customer","device"]

admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Account)
admin.site.register(Order,Admin)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Processor)
admin.site.register(Filters,Admin) 