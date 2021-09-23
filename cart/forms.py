from django import forms 
from django.forms import NumberInput
from django.forms.fields import CharField
# from django.core import validators

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField( min_value=1, widget=NumberInput(attrs={'class': 'form-control text-center','value': 1, 'max':20 }))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    attribute_1= forms.CharField(required=False)
    attribute_2= forms.CharField(required=False)
    attribute_3= forms.CharField(required=False)
    # def __init__(self, *args, **kwargs):
    #     try:
    #         extra = kwargs.pop('extra')
    #         if not extra:
    #             extra_fields = 0
    #         super(CartAddProductForm, self).__init__(*args, **kwargs)
    #         self.fields['all_atributes'].initial = extra_fields
    #         print('extra fieself.fields[]lds', self.fields['all_atributes'].initial)
    #         for index in enumerate(extra):
    #             self.fields['attribute_{index}'.format(index=index)] = forms.CharField()
    #             print('extra fields', self.fields['attribute_{index}'.format(index=index)])
    #     except:
    #         print('except form')

class CartUpdateProductQuantityForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput)
    quantity = forms.IntegerField(min_value=1)



