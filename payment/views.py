import re
import json
import requests
from django.shortcuts import render, redirect
from payment.forms import PostMach, PostPay, PostWebpay, PostMercadoPago
from django.http import HttpResponse
import urllib3
    
pool = urllib3.PoolManager()

#MAIN
# API_URL_BASE = 'https://us-central1-cl-8pay.cloudfunctions.net/API/'
# UPI_URL_BASE = 'https://us-central1-cl-8pay.cloudfunctions.net/UPI/'
# WEBHOOK_URL_BASE = 'https://us-central1-cl-8pay.cloudfunctions.net/WEBHOOK/'

#TEST
API_URL_BASE = "https://us-central1-dev-upi-cl.cloudfunctions.net/API/" #'http://localhost:5001/dev-upi-cl/us-central1/API/'
UPI_URL_BASE = "https://us-central1-dev-upi-cl.cloudfunctions.net/UPI/" #'http://localhost:5001/dev-upi-cl/us-central1/UPI/'
WEBHOOK_URL_BASE = "https://us-central1-dev-upi-cl.cloudfunctions.net/WEBHOOK/" #'http://localhost:5001/dev-upi-cl/us-central1/WEBHOOK/'

# ---------------------------------------------------------------- #
# -----------------------------VISTAS----------------------------- #
# ---------------------------------------------------------------- #

# ----------------------------PÚBLICAS---------------------------- #
# def index(request):
# return render(request, 'payment/index.html')

def ticket(request, ticket_id):
    ticket = getTicketData(ticket_id)
    
    if ticket.status_code == 200:
        tdjson = json.loads(ticket.text)
        ticket_data = tdjson["response"]
        businessd = getBusinessData(ticket_data["bid"])
        bdjson = json.loads(businessd.text)

        data = {
            "ticket_id": ticket_id,
            "productos": getProductsData(ticket_data["productos"]),
            "amount": 0,
            "business_name" : bdjson["name"],
            "business_logo" : bdjson["logo"]
        }

        if (request.method == "POST"):
            body = request.body.decode('utf-8')

            payment = createPaymentRequest(body)
            pdjson = json.loads(payment.text)
            payment_id = pdjson['pid']

            if (payment.status_code == 200):
                return redirect(f'/p/{payment_id}')
            else:
                return render(request, 'error/not_found.html', {
                    "codigo": payment.status_code,
                    "mensaje": "Estamos teniendo dificultades técnicas!",
                    "detalle": "Favor vuelve a intentar nuevamente. Contáctate con el comercio y solicitale una url válida."
                })

        return render(request, 'payment/ticket.html', { 'datos': data })
    elif ticket.status_code == 404:
        return render(request, 'error/not_found.html', {
            "codigo": "404",
            "mensaje": "Al parecer estas perdido!",
            "detalle": "La boleta que estas buscando no existe. Contáctate con el comercio y solicitale una url válida."
        })
    else:
        print(ticket.status_code)
        return render(request,'error/not_found.html', {
            "codigo" : "500",
            "mensaje" : "Estamos teniendo dificultades técnicas!",
            "detalle" : "Favor vuelve a intentar nuevamente. Si el error perciste contáctate con el comercio."
        })

def payment(request, payment_id):
    # (1) VERIFICAR QUE EXISTA EL COBRO
    # (2) VERIFICAR QUE ESTÉ PENDIENTE DE PAGO
    # (3) OBTENER DATOS DEL NEGOCIO

    #(1)
    paymentd = getPaymentData(payment_id)
    if paymentd.status_code == 200:
        # EL COBRO EXISTE
        #(1)...
        pdjson = json.loads(paymentd.text)
        #(2)
        if pdjson["status"] == 'pending':
            # AÚN NO HA SIDO COBRADO
            #(3)
            businessd = getBusinessData(pdjson["business"])
            bdjson = json.loads(businessd.text)
            
            return render(request, 'payment/index.html',{
                    "isMobile" : isMobile(request),
                    "title" : pdjson["title"],
                    "description" : pdjson["description"],
                    "business_order_numer" : pdjson["business_order_number"],
                    "amount" : pdjson["total_amount"],
                    "paymentid" : payment_id,
                    "business_name" : bdjson["name"],
                    "business_logo" : bdjson["logo"]
            })
        else:
            return render(request,'error/not_found.html', {
                    "codigo" : "200",
                    "mensaje" : "Al parecer estás perdido!",
                    "detalle" : "El pago que estás intentando pagar ya fue cancelado"
            })
    elif paymentd.status_code == 404:
        return render(request,'error/not_found.html', {
                    "codigo" : "404",
                    "mensaje" : "Al parecer estás perdido!",
                    "detalle" : "El pago que estás buscando no existe. /nContáctate con el comercio y solicitale una url válida."
        })
    else:
        return render(request,'error/not_found.html', {
                    "codigo" : "500",
                    "mensaje" : "Estamos teniendo dificultades técnicas!",
                    "detalle" : "Favor vuelve a intentar nuevamente. /nSi el error persiste contáctate con el comercio."
        })

def payedWebpay(request):
    token = request.GET.get('token_ws')
    response = validateWebpayTransaction(token)
    if response == 200:
        return render(request, 'payment/success_transaction.html',{
            'site_redirect_url': 'https://sumonttiauditores.com/'
        })
    else:
        return render(request, 'payment/fail_transaction.html')

def webpay(request, token):
    return render(request, 'payment/webpay.html',
                {
                    "url" : 'https://webpay3g.transbank.cl:443/webpayserver/initTransaction',
                    "token" : token
                }
            )

def match(request, token):
    return render(request, 'payment/webpay.html',
                {
                    "url" : 'https://webpay3gint.transbank.cl/webpayserver/initTransaction',
                    "token" : token
                }
            )

def checkPayment(request, payment_id):
    return render(request, 'payment/index.html')

def dashboard(request):
    print('redirect to dashboard')
    return render(request, 'dashboard/index.html')

def collect(request):
    return render(request, 'collect/index.html')

# ---------------------------------------------------------------- #
# ---------------------------HTML FORMS--------------------------- #
# ---------------------------------------------------------------- #
# PAY WEBPAY
def postPayWebpay(request, payment_id):
    print('init webpay')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostWebpay(request.POST)
        # check whether it's valid:
        if form.is_valid():           
            djson = pay(request, 'webpay', payment_id, 'py')
            if djson != 400:    
                return render(request, 'payment/webpay.html',{
                    "url" : djson['data']['url'],
                    "token" : djson['data']['token']
                })
            else:
                print('NO OK')
                print(djson)
                return HttpResponse('<H1>Error en el formulario</H1>')
            
        else:
            print('No es valido')
            return HttpResponse('<H1>Error en el formulario</H1>')
    else:
        return HttpResponse('<H1>Error en el formulario</H1>')
    
# PAY MACH
def postPayMach(request, payment_id):
    print('init mach')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostMach(request.POST)
        # check whether it's valid:
        if form.is_valid():           
            deep_link = pay(request, 'mach', payment_id, 'py')
            if deep_link != 400:
                response = HttpResponse("", status=302)
                response['Location'] = deep_link['url']
                return response
            else:
                print('NO OK')
                print(deep_link)
                return HttpResponse('<H1>Error en el formulario</H1>')
            
        else:
            print('No es valido')
            return HttpResponse('<H1>Error en el formulario</H1>')
    else:
        return HttpResponse('<H1>Error en el formulario</H1>')
    
# PAY MERCADOPAGO
def postPayMercadoPago(request, payment_id):
    print('init mercadopago')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostMercadoPago(request.POST)
        # check whether it's valid:
        if form.is_valid():           
            djson = pay(request, 'mercadopago', payment_id, 'py')
            if djson != 400:
                response = HttpResponse("", status=302)
                response['Location'] = djson['url']
                return response
                # return render(request, 'payment/webpay.html',{
                #     "url" : djson['data']['url'],
                #     "token" : djson['data']['token']
                # })
            else:
                print('NO OK')
                print(djson)
                return HttpResponse('<H1>Error en el formulario</H1>')
            
        else:
            print('No es valido')
            return HttpResponse('<H1>Error en el formulario</H1>')
    else:
        return HttpResponse('<H1>Error en el formulario</H1>')
    
# PAY
def postPay(request, payment_id):
    print('init postPay()')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostPay(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print(form.cleaned_data['payment_method'])
            return HttpResponse('<H1>Logrado</H1>')
        else:
            print('No es valido')
            return HttpResponse('<H1>Error en el formulario</H1>')
    else:
        return HttpResponse('<H1>Error en el formulario</H1>')
    

# ---------------------------------------------------------------- #
# --------------------FUNCIONES CONECCIÓN UPI--------------------- #
# ---------------------------------------------------------------- #
def getPaymentData(payment_id):
    url = UPI_URL_BASE+"payment/"+payment_id
    payload={}
    headers={}
    return requests.request("GET", url, headers=headers, data=payload)

def pay(request, method, payment_id, to):
    url = UPI_URL_BASE+"pay/"+method+"/"+str(payment_id)
    payload={}
    headers={}
    try:
        response =  requests.request("POST", url, headers=headers, data=payload)
        print(response)
        print(response.text)
        if response.ok:
            data = response.text
            print('RESPONSE:')
            print(data)
            jsonResponse = json.loads(data)
            return jsonResponse['data']
        else:
            return response.status_code
    except IndexError:
        print(IndexError)
        return HttpResponse(500)
    except AttributeError:
        print(AttributeError)
        return HttpResponse(500)

def validateWebpayTransaction(token):
    url = WEBHOOK_URL_BASE+"webpay/?token_ws="+token
    payload={}
    headers={}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.status_code

def createPaymentRequest(payment_data):
    url = UPI_URL_BASE+'payment'
    headers={
        "tipo-transaccion": "pago",
        "metodologia-cobro": "link",
        "content-type": "application/json",
        "Authorization": "Bearer U2FsdGVkX1/MjlmVi1GpGJkt9GQpXn4F3iempb/vR7dBSZzTNP6k2whtbky3x8iR"
    }
    return requests.request("POST", url, data=payment_data, headers=headers)

# ---------------------------------------------------------------- #
# --------------------FUNCIONES CONECCIÓN API--------------------- #
# ---------------------------------------------------------------- #
def getBusinessData(business_id):
    url = API_URL_BASE+"user/"+business_id
    payload={}
    headers={}
    return requests.request("GET", url, headers=headers, data=payload)

# OBTENER LA INFORMACIÓN DEL TICKET
def getTicketData(ticket_id):
    url = API_URL_BASE+"ticket/"+ticket_id
    payload={}
    headers={
        'Authorization': 'Bearer U2FsdGVkX1/MjlmVi1GpGJkt9GQpXn4F3iempb/vR7dBSZzTNP6k2whtbky3x8iR',
    }
    return requests.request("GET", url, headers=headers, data=payload)

# OBTENER LOS PRODUCTOS DEL TICKET
def getProductsData(products):
    pendings = []
    id = 0
    for product in products:
        pending_amount = (product['precio'] * product['cantidad'] - product['payed_amount']) / product['precio']
        product['id'] = id
        id = id + 1
        for i in range(int(pending_amount)):
            pendings.append(product)
    return pendings
    

# ---------------------------------------------------------------- #
# ------------------------HANDLE RESPONSE------------------------- #
# ---------------------------------------------------------------- #
def isMobile(request):
    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False
    
def handleResponse(response):
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return response.status_code