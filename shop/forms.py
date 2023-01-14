import json

from django import forms
from django.utils.translation import gettext_lazy as _

from shop.models import Item
from shop.widgets import ItemOptionwidget

class AdminItemForm(forms.ModelForm):

    class Meta:
        models = Item
        fields = [
            'category', 'name', 'slug', 'description', 
            'supply_amount', 'amount', 'tax', 'sale_percent', 'sale_amount', 
            'stock', 'is_halal', 'is_public','best_item', 'options'
        ]

        widgets = {'options': ItemOptionwidget}