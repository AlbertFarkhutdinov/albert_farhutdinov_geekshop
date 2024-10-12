from django import forms
from shop.main_app.models import ProductCategory


class ProductCategoryEditForm(forms.ModelForm):
    discount = forms.IntegerField(label='Discount', required=False, min_value=0, max_value=90, initial=0)

    class Meta:
        model = ProductCategory
        exclude = ()
