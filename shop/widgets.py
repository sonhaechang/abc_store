from django import forms

class ItemOptionwidget(forms.TextInput):
    template_name = 'widgets/item_options_widget.html'

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs['hidden'] = True
        return attrs