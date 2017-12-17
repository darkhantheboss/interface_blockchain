from django import forms
from .models import TransactionContract

class TransactionContractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransactionContractForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TransactionContract
        fields = ('sender', 'receiver', 'contract')
        widgets = {
            'sender': forms.HiddenInput(),
        }
