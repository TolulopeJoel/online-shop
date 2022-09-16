from django import forms

PRICE_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class AddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRICE_QUANTITY_CHOICES, coerce=int)
    overide = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)