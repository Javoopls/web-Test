#import pyrebase
import json
import requests

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from .forms import PostBusinessRegistration
from dashboard.views import index

API_URL_BASE =  'https://us-central1-cl-8pay.cloudfunctions.net/API/' #"https://us-central1-dev-upi-cl.cloudfunctions.net/API/" #'http://localhost:5001/dev-upi-cl/us-central1/API/'

# ==================================================================== #
#                                 VIEWS                                #
# ==================================================================== #
def login(request):
    return render(request, 'login/login.html')
  
def register(request):
    return render(request, 'login/register.html')

def succes_register(request):
    return render(request, 'login/succes_registration.html')

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_urk = fs.url(filename)
        return login(request)
    
    return register(request)


# ==================================================================== #
#                                 FORMS                                #
# ==================================================================== #

def postCommerceRegistration(request):
    print('init post Commerce Registration')
    if request.method == 'POST':
        form = PostBusinessRegistration(request.POST)
        if form.is_valid():            
            payload = json.dumps({
                "com_razon_social": form.cleaned_data['razon_social'],
                "com_tipo": form.cleaned_data['tipo_sociedad'],
                "com_rut": form.cleaned_data['rut_sociedad'],
                "com_giro": form.cleaned_data['giro_sociedad'],
                "com_correo": form.cleaned_data['correo_sociedad'],
                "com_direccion": form.cleaned_data['direccion_sociedad'],
                "com_telefono": form.cleaned_data['telefono_sociedad'],
                "bco": form.cleaned_data['banco_sociedad'],
                "bco_ncuenta": form.cleaned_data['numero_cta_banco'],
                "bco_tipo_cta": form.cleaned_data['tipo_cta_banco'],
                "rl_nombre": form.cleaned_data['nombre_rl'],
                "rl_apaterno": form.cleaned_data['apaterno_rl'],
                "rl_amaterno": form.cleaned_data['amaterno_rl'],
                "rl_run": form.cleaned_data['run_rl'],
                "rl_correo": form.cleaned_data['correo_rl'],
                "rl_telefono": form.cleaned_data['telefono_rl']
            })
            headers = {
                #'password': form.cleaned_data['password'],
                'Content-Type': 'application/json'
            }
            
            cid = createCommerce(payload, headers)
            print(cid.text)
            return render(request, 'login/succes_registration.html')
        else:
            return render(request,'error/404.html',{
                "error_code": "400",
                "error_msg": "Error en el formulario"
            })
    else:
        form = PostBusinessRegistration()
        return render(request,'error/404.html',{
                "error_code": "500",
                "error_msg": "Error interno. Intente nuevamente más tarde."
            })



# ==================================================================== #
#                                  API                                 #
# ==================================================================== #
#CREAR COMMERCE
def createCommerce(payload, headers):
    url = API_URL_BASE+"user/commerce"
    return requests.request("POST", url, headers=headers, data=payload)



# ---------------------------------------------------------------- #
# --------------------------- FIREBASE --------------------------- #
# ---------------------------------------------------------------- #

#here we are doing firebase authentication
# firebase=pyrebase.initialize_app(firebaseConfig)
# auth = firebase.auth()
# database=firebase.database()

# def authenticate(email, password):
#     print("Auth init")
#     # Log the user in
#     try:
#         user = auth.sign_in_with_email_and_password(email, password)
#         print(user)
#     except:
#         print("Error")