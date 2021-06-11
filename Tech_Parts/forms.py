from django import forms
from .models import *


class AddForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=["products"]

class TypeFilter(forms.ModelForm):
    class Meta:
        model=Filters
        fields=["type"]
        
class CategoryFilter(forms.ModelForm):
    class Meta:
        model=Filters
        fields=["category"]
           
class ProcessorFilter(forms.ModelForm):
    class Meta:
        model=Filters
        fields=["processor"]
       
class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=["products"]
       
class DashboardForm(forms.ModelForm):
    class Meta:
        model=Product
        exclude=["code","slug"]
       
# class Result(forms.ModelForm):
#     class Meta:
#         model=