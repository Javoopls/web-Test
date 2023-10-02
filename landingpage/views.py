from django.shortcuts import render

# ---------------------------------------------------------------- #
# -----------------------------VISTAS----------------------------- #
# ---------------------------------------------------------------- #

# ----------------------------PÚBLICAS---------------------------- #
def index(request):
    return render(request, 'landingpage/index.html')

def login(request):
    return render(request, 'login/index.html')

def dashboard(request):
    return render(request, 'dashboard/index.html')

def paymentMethods(request):
    return render(request, 'payment/index.html')