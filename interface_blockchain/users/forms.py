from django import forms
from .models import Contract, Responsibility


class ContractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Contract
        fields = ('creator', 'name', 'total_amount')
        widgets = {
            'creator': forms.HiddenInput(),
        }


class ResponsibilityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ResponsibilityForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Responsibility
        fields = ('contract', 'name')
        widgets = {
            'contract': forms.HiddenInput(),
        }
