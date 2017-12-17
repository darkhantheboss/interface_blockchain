from django import forms
from .models import Product, Good


class GoodForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GoodForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Good
        fields = ('name', 'options', 'description', 'image', 'tmp_responsibility', 'tmp_amount')
        widgets = {
            'tmp_responsibility': forms.HiddenInput(),
        }
