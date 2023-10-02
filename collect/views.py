import json
import requests
from urllib import request

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import PostVerifyID, PostNewCollect

API_URL_BASE =  'https://us-central1-cl-8pay.cloudfunctions.net/API/' #"https://us-central1-dev-upi-cl.cloudfunctions.net/API/" #'http://localhost:5001/dev-upi-cl/us-central1/API/'
UPI_URL_BASE =  'https://us-central1-cl-8pay.cloudfunctions.net/UPI/' #"https://us-central1-dev-upi-cl.cloudfunctions.net/UPI/" #'http://localhost:5001/dev-upi-cl/us-central1/UPI/'

# ==================================================================== #
#                                 VIEWS                                #
# ==================================================================== #
def index(request, uid, state):
    return render(request, 'collect/index.html',{
        'uid': uid,
        'state_form': state
    })

def verify(request):
    return render(request, 'collect/verify.html')

# ==================================================================== #
#                                 FORMS                                #
# ==================================================================== #
def postVerifyUid(request):
    if request.method == 'POST':
        form = PostVerifyID(request.POST)
        if form.is_valid():
            cid = form.cleaned_data['uid']
            if validateCommerce(cid) == 200:
                return index(request, cid, '')
            else:
                return HttpResponse('<H1>Usuario Inválido</H1>')            
    else:
        form = PostVerifyID()
    return HttpResponse('<H1>Error en el formulario</H1>')

def postNewCollect(request, bid):
    if request.method == 'POST':
        form = PostNewCollect(request.POST)
        
        if form.is_valid():
            headers = {
                'to': form.cleaned_data['email'],
                'bid': bid,
                'client': form.cleaned_data['name'],
                'amount': form.cleaned_data['amount'],
                'detail': form.cleaned_data['description'],
                'order_number': form.cleaned_data['order_number'],
                'commmerceName': 'Sumotti Auditores'
            }
            response = sendMailPayment(headers)
            print(response.text)
            if response.status_code == 200:
                form.clean()
                return index(request, bid, 'exitoso')
            else:
                form.clean()
                return index(request, bid, 'erroneo')
        else:
            form.clean()
            return HttpResponse('<H1>Error en el formulario</H1>')

    else:
        form = PostNewCollect()
        form.clean()
    return HttpResponse('<H1>Error en el formulario</H1>')

# ==================================================================== #
#                                  API                                 #
# ==================================================================== #
def validateCommerce(cid):
    url = API_URL_BASE+"user/commerce/validate/"+cid
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.status_code


def sendMailPayment(headers):
    # Envío del correo            
    url = API_URL_BASE+"mailer/"
    payload = json.dumps({
        "monto_total": headers['amount'],
        "titulo": "Cobro Sumontti a "+headers['client'],
        "descripcion": headers['detail'],
        "return_url": "https://www.sumonttiauditores.com/",
        "business_order_number": headers['order_number'],
        "commmerceName": headers['commmerceName']
    })
    headers = {
        'to': headers['to'],
        'bid': headers['bid'],
        'client': headers['client'],
        'detail': headers['detail'],
        'Content-Type': 'application/json'
    }
    return requests.request("POST", url, headers=headers, data=payload)


# def handler404(request, exception, template_name="error/404.html"):
#     response = render_to_response(template_name)
#     response.status_code = 404
#     return response