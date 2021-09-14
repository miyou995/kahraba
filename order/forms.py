from django import forms 
from django.forms import NumberInput
# from django.core import validators
from .models import Order
from delivery.models import Commune


class OrderCreateForm(forms.ModelForm):
    # quantity = forms.IntegerField(min_value=1)
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'campany', 'email', 'phone', 'wilaya', 'commune', 'note']
        required = ('first_name', 'last_name',  'phone', 'wilaya', 'commune')
       

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['wilaya'] = forms.ModelChoiceField(queryset=Wilaya.objects.all()) 
        # self.fields['commune'] = forms.ModelChoiceField(queryset=Commune.objects.all()) 

        self.fields['commune'].queryset = Commune.objects.none()
        # self.fields['quantity'] = forms.IntegerField(min_value=1)

        if 'wilaya' in self.data:
            try:
                wilaya_id = int(self.data.get('wilaya'))
                self.fields['commune'].queryset = Commune.objects.filter(wilaya_id=wilaya_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif not 'wilaya' in self.data:
            self.fields['commune'].queryset = Commune.objects.none()

class OrderFormWithQuantity(OrderCreateForm):
    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['quantity'] = forms.IntegerField(min_value=1)


