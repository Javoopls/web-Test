from django import forms


class GenerateApiKey(forms.Form):
    pass

class PostNewCollect(forms.Form):
    name = forms.CharField(label='name', max_length=50)
    email = forms.CharField(label='email', max_length=50)
    amount = forms.CharField(label='amount')
    description = forms.CharField(label='description', max_length=500)
    description2 = forms.CharField(label='description2', required=False, max_length=500)
    description3 = forms.CharField(label='description3', required=False, max_length=500)
    order_number = forms.CharField(label='order_number', max_length=500)

class NewApiKey(forms.Form):
    pass
