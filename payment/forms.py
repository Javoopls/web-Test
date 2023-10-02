from django import forms

class PostWebpay(forms.Form):
    pass
    
class PostMach(forms.Form):
    pass

class PostMercadoPago(forms.Form):
    pass

class PostPay(forms.Form):
    def clean(self):
        print(self)
        if 'paywebpay' in self.data:
            # do subscribe
            print('webpay')
            return 'webpay'
        elif 'paymach' in self.data:
            # do unsubscribe
            print('mach')
            return 'mach'
        elif 'paymercadopago' in self.data:
            # do unsubscribe
            print('mercadopago')
            return 'mercadopago'
        else:
            return '404'