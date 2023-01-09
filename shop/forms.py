import json

from django import forms
from django.utils.translation import gettext_lazy as _

from shop.models import Item
from shop.widgets import ItemOptionwidget

class AdminItemForm(forms.ModelForm):
    options = forms.CharField(
        # _(u'옵션 선택'),
        required=False,
        widget=ItemOptionwidget,
    )

    class Meta:
        models = Item
        fields = [
            'category', 'name', 'slug', 'description', 
            'supply_amount', 'amount', 'tax', 'sale_percent', 'sale_amount', 
            'stock', 'is_halal', 'is_public','best_item', 'options'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        try:
            item_dict = dict()
            for item in self.instance.itemoption_item.all():
                if item.name in item_dict:
                    item_dict[item.name].append(item.value)
                else:
                    item_dict[item.name] = [item.value]

            self.fields['options'].initial = json.dumps(item_dict)
        except ValueError:
            pass