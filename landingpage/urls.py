from . import views as main_views
from django.urls import path, include
from .views import index, dashboard, paymentMethods, login


urlpatterns = [
    # ----------------------------------------------------------------- #
    # ---------------------------- VISTAS ----------------------------- #
    # ----------------------------------------------------------------- #
    
    # REDIRECCIÓN APLICACIONES
    path('', include('payment.urls') ),
    path('', include('dashboard.urls') ),
    
    
    # WELCOME
    path('',index, name="index"),
    path('index/',index, name="index"),
    path('login/',login, name="login"),
    path('landingpage/',index, name="index"),
    path('dashboard/',dashboard, name="dashboard"),
    path('payment/1661326023330',paymentMethods, name="paymentMethods"),
    
    
    
    
    # ----------------------------------------------------------------- #
    # ---------------------------- MÉTODOS ---------------------------- #
    # ----------------------------------------------------------------- #
]
