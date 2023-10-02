from . import views as main_views
from django.urls import path, include
from .views import pay, payment, webpay, payedWebpay, ticket


urlpatterns = [
    # ----------------------------------------------------------------- #
    # ---------------------------- VISTAS ----------------------------- #
    # ----------------------------------------------------------------- #
    
    # REDIRECCIÓN APLICACIONES

    path('collect/', include('collect.urls')),
    path('dashboard/', include('dashboard.urls')),
    
    # WELCOME
    path('<str:payment_id>/',payment, name="payment"),
    path('t/<str:ticket_id>/',ticket, name=""), # <- ticket
    path('payment/webpay/<str:token>',webpay, name="webpay"),
    path('payed/webpay/',payedWebpay, name="payedWebpay"),
    # path('payment/match/<str:token>',match, name="payment"),
    # path('payment/waiting_transacction/<str:payment_id>',match, name="payment"),
    
    
    
    # ----------------------------------------------------------------- #
    # ---------------------------- MÉTODOS ---------------------------- #
    # ----------------------------------------------------------------- #
    
    path('pay/<str:method>/<str:payment_id>/<str:to>',pay, name="pay"),
    
    # PAGOS
    path('postPayWebpay/<str:payment_id>/', main_views.postPayWebpay, name="postPayWebpay"),
    path('postPayMach/<str:payment_id>/', main_views.postPayMach, name="postPayMach"),
    path('postPayMercadoPago/<str:payment_id>/', main_views.postPayMercadoPago, name="postPayMercadoPago"),
]
