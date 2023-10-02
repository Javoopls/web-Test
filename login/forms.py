from django import forms


class PostBusinessRegistration(forms.Form):
    razon_social = forms.CharField(label='razon_social', max_length=100)
    tipo_sociedad = forms.CharField(label='tipo_sociedad', max_length=100)
    rut_sociedad = forms.CharField(label='rut_sociedad', max_length=100)
    giro_sociedad = forms.CharField(label='giro_sociedad', max_length=100)
    direccion_sociedad = forms.CharField(label='direccion_sociedad', max_length=100)
    correo_sociedad = forms.EmailField(label='correo_sociedad')
    telefono_sociedad = forms.CharField(label='telefono_sociedad', max_length=100)
    #estatutos = forms.CharField(label='estatutos', max_length=100)
    #certificado_vigencia_estatutos = forms.CharField(label='certificado_vigencia_estatutos', max_length=100)
    
    banco_sociedad = forms.CharField(label='banco_sociedad', max_length=100)
    numero_cta_banco = forms.CharField(label='numero_cta_banco', max_length=100)
    tipo_cta_banco =forms.CharField(label='tipo_cta_banco', max_length=100)
    
    nombre_rl = forms.CharField(label='nombre_rl', max_length=100)
    apaterno_rl = forms.CharField(label='apaterno_rl', max_length=100)
    amaterno_rl = forms.CharField(label='amaterno_rl', max_length=100)
    run_rl = forms.CharField(label='run_rl', max_length=100)
    correo_rl = forms.EmailField(label='correo_rl')
    telefono_rl = forms.CharField(label='telefono_rl', max_length=100)
    
    #plan_suscripcion = forms.CharField(label='plan_suscripcion', max_length=100)