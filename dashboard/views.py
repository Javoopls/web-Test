import json
import requests
import time
import qrcode

from platform import java_ver
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse

from dashboard.forms import GenerateApiKey, PostNewCollect
from dashboard.forms import GenerateApiKey, NewApiKey
from payment.models import Payment
from datetime import date, datetime
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse


#API_URL_BASE =  'https://us-central1-cl-8pay.cloudfunctions.net/API/' #"https://us-central1-dev-upi-cl.cloudfunctions.net/API/" #'http://localhost:5001/dev-upi-cl/us-central1/API/'
#UPI_URL_BASE =  'https://us-central1-cl-8pay.cloudfunctions.net/UPI/' #"https://us-central1-dev-upi-cl.cloudfunctions.net/UPI/" #'http://localhost:5001/dev-upi-cl/us-central1/UPI/'

#TEST
API_URL_BASE = "https://us-central1-dev-upi-cl.cloudfunctions.net/API/" #'http://localhost:5001/dev-upi-cl/us-central1/API/'
UPI_URL_BASE = "https://us-central1-dev-upi-cl.cloudfunctions.net/UPI/" #'http://localhost:5001/dev-upi-cl/us-central1/UPI/'

# ==================================================================== #
#                                 VIEWS                                #
# ==================================================================== #
def index(request):
    return render(request, 'dashboard/index.html')

def login(request):
    return render(request, 'dashboard/login.html')

def register(request):
    print('init register')
    return render(request, 'dashboard/register2.html')

def apikeys(request):
    apikey = getApiKey()
    apikeys = [apikey]
    return render(request, 'dashboard/apikeys.html', {"apikeys" : apikeys})

def mailling_collect(request):
    return render(request, 'dashboard/mailling_collect.html')

def mailling_collect2(request, state):
    return render(request, 'dashboard/mailling_collect.html', {'state_form': state})

def masive_mailling_collect(request):
    return render(request, 'dashboard/masive_mailling_collect.html')

def profile(request):
    return render(request, 'dashboard/profile.html')

def form_tecnico(request):
    return render(request, 'dashboard/form_tecnico.html')

def negocio_historial(request):
    # Obtener las fechas de inicio y fin del formulario
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Filtrar ventas por fechas si se proporcionan
    if fecha_inicio and fecha_fin:
        try:
            # Convierte las fechas de cadena a objetos de fecha si es necesario
            fecha_inicio = date.fromisoformat(fecha_inicio)
            fecha_fin = date.fromisoformat(fecha_fin)

            # Filtra ventas en el rango de fechas
            ventas = Payment.objects.filter(created_at__date__range=[fecha_inicio, fecha_fin])
        except ValueError:
            # Maneja errores de formato de fecha aquí si es necesario
            # Puedes mostrar un mensaje de error o realizar alguna otra acción
            ventas = []
    else:
        # Obtener todas las ventas si no se proporcionan fechas
        ventas = Payment.objects.all()

    return render(request, 'dashboard/negocio_historial.html', {"ventas": ventas})

def negocio_historial_since(request, since):
    ventas = getVentas(since)
    return render(request, 'dashboard/negocio_historial.html', {"ventas" : ventas})

def negocio_metricas(request):
    metricas = getMetricas(None, None, '1679398566500')
    labels = []
    data = []

    for dia_data in metricas:
        labels.append(dia_data["day"])
        data.append(dia_data["total_sales"])
        
    # Calcular la suma total de total_transactions
    suma_total_iva = sum(item["total_iva"] for item in metricas)
    suma_total_sales = sum(item["total_sales"] for item in metricas)
    suma_total_earnings = sum(item["total_earnings"] for item in metricas)
    suma_total_commissions = sum(item["total_commissions"] for item in metricas)
    suma_total_transactions = sum(item["total_transactions"] for item in metricas)

    # Insertar la suma en un nuevo diccionario
    suma_periodo = {
        "date": "TOTAL PERIODOD",
        "total_iva": suma_total_iva,
        "total_sales": suma_total_sales,
        "total_earnings": suma_total_earnings,
        "total_commissions": suma_total_commissions,
        "total_transactions": suma_total_transactions
    }

    # Agregar el nuevo dato al final de la lista "data"
    metricas.append(suma_periodo)
        
    return render(request, 'dashboard/negocio_metricas.html', {
        "metricas" : metricas,
        "labels" : labels,
        "data" : data,
    })

def blockdeprueba(request):
    return render(request, 'dashboard/blockdeprueba.html')


# ==================================================================== #
#                                 FORMS                                #
# ==================================================================== #
def postGenerateApiKey(request):
    return 0

def getNewApiKey(request):
    return render(request, 'dashboard/getNewApiKey.html')


def newApiKey(request):
    print("INIT GET NEW APIKEY")
    if request.method == 'POST':
        form = NewApiKey(request.POST)
        if form.is_valid(): 
            apikey = newApiKeySearch()
            apikeys = [apikey]
            print(apikey)
            return getNewApiKey(request,apikeys)
        else:
            print('NO OK')
            return HttpResponse('<H1>Error en el formulario 1</H1>')
    else:
        return HttpResponse('<H1>Error en el formulario 2</H1>')


def postNewCollect(request):
    print("INIT POSTGENERATE")
    if request.method == 'POST':
        form = PostNewCollect(request.POST)
        
        if form.is_valid():
            description = form.cleaned_data['description']
            description2 = form.cleaned_data.get('description2', '')  # Valor por defecto vacío si no se proporciona
            description3 = form.cleaned_data.get('description3', '')  # Valor por defecto vacío si no se proporciona

            # Crea el array 'detail' con los datos
            detail = [description]
            if description2:
                detail.append(description2)
            if description3:
                detail.append(description3)
                
            headers = {
                'to': form.cleaned_data['email'],
                'bid': "-",
                'client': form.cleaned_data['name'],
                'total_amount': form.cleaned_data['amount'],
                'detail': detail,
                'order_number': form.cleaned_data['order_number'],
                'commmerceName': 'Contadores de Chile'
            }
            response = sendMailPayment(headers)
            if response.status_code == 201:
                form.clean()
                return mailling_collect2(request, 'exitoso')
            else:
                form.clean()
                return mailling_collect2(request, 'erroneo')
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
def getApiKey():
    url = "https://us-central1-dev-upi-cl.cloudfunctions.net/API/api-key/"
    payload={}
    headers = {'uid': 'ovIG4z8tBjohZP06ONFC'}
    print("INIT GET APIKEY")
    try:
        response = requests.request("POST", url, headers=headers, data=payload) 
        if response.ok:
            print(response)
            return response.text
        else:
            return HttpResponse(400)
    except AttributeError:
        print(AttributeError)
        return HttpResponse(500)
    
def sendMailPayment(headers):
    # Envío del correo            
    url = API_URL_BASE+"mailer/"
    payload = json.dumps({
        "total_amount": headers['total_amount'],
        "title": "Cobro Sumontti a "+headers['client'],
        "description": headers['detail'],
        "return_url": "-",
        "collection_detail": headers['detail'],
        "business_order_number": headers['order_number'],
    })
    headers = {
        'to': headers['to'],
        'from': headers['commmerceName'],
        'bid': headers['bid'],
        'client': headers['client'],
        'Content-Type': 'application/json'
    }
    return requests.request("POST", url, headers=headers, data=payload)


def newApiKeySearch():
    url = "https://us-central1-dev-upi-cl.cloudfunctions.net/API/api-key/"
    payload={}
    headers = {'uid': 'ovIG4z8tBjohZP06ONFC'}
    print("INIT NEW APIKEY")
    try:
        response = requests.request("POST", url, headers=headers, data=payload) 
        if response.ok:
            print(response)
            return response.text
        else:
            return HttpResponse(400)
    except AttributeError:
        print(AttributeError)
        return HttpResponse(500)

def getVentas(since):
    url = API_URL_BASE+"payments/record/"
    if since != None:
        headers = {
            'authorization': 'Bearer U2FsdGVkX1+MfaVMzT7irNReILD16UuiqJTw5YAigFRmaBMfup4knvvwulPXnvmT',
            'from': since
        }
    else:
        headers = {
            'authorization': 'Bearer U2FsdGVkX1+MfaVMzT7irNReILD16UuiqJTw5YAigFRmaBMfup4knvvwulPXnvmT',
        }
    response = requests.request("GET", url, headers=headers, data={}) 
    if response.ok:
        jsonResponse = response.json()
        return jsonResponse.get('data')
    else:
        return ""
    
def getMetricas(day, week, month):
    url = API_URL_BASE+"payments/metrics/"
    if day != None:
        headers = {
            'authorization': 'Bearer U2FsdGVkX1+MfaVMzT7irNReILD16UuiqJTw5YAigFRmaBMfup4knvvwulPXnvmT',
            'day': day
        }
    elif week != None:
        headers = {
            'authorization': 'Bearer U2FsdGVkX1+MfaVMzT7irNReILD16UuiqJTw5YAigFRmaBMfup4knvvwulPXnvmT',
            'week': week
        }
    elif month != None:
        headers = {
            'authorization': 'Bearer U2FsdGVkX1+MfaVMzT7irNReILD16UuiqJTw5YAigFRmaBMfup4knvvwulPXnvmT',
            'month': month
        }
    else:
        headers = {
            'authorization': 'Bearer U2FsdGVkX1+MfaVMzT7irNReILD16UuiqJTw5YAigFRmaBMfup4knvvwulPXnvmT',
        }
    response = requests.request("GET", url, headers=headers, data={}) 
    if response.ok:
        jsonResponse = response.json()
        return jsonResponse.get('data')
    else:
        return ""
    
    
def generar_y_mostrar_qr(request):
    # Datos que quieres codificar en el código QR
    datos_para_qr = "https://futbollibre.futbol/"

    # Generar el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(datos_para_qr)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar la imagen en un archivo (opcional)
    img.save("codigo_qr.png")

    # Mostrar el código QR en la plantilla HTML
    return render(request, 'dashboard/qr_template.html', {'img': img})




