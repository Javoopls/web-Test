from django import forms

class PostVerifyID(forms.Form):
    uid = forms.CharField(label='uid', max_length=50)
    
class PostNewCollect(forms.Form):
    name = forms.CharField(label='name', max_length=50)
    email = forms.CharField(label='email', max_length=50)
    amount = forms.CharField(label='amount')
    description = forms.CharField(label='description', max_length=500)
    order_number = forms.CharField(label='order_number', max_length=500)
    