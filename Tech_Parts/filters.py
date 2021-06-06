import django_filters
from django.forms.widgets import CheckboxSelectMultiple

from .models import *

class Filter(django_filters.FilterSet):
    category__name=django_filters.ModelMultipleChoiceFilter(widget=CheckboxSelectMultiple,queryset=Category.objects.all())
    class Meta:
        model=Product
        fields=["category"]
 
 
 