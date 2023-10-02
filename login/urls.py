from . import views as main_views
from django.urls import path
from .views import login, register, postCommerceRegistration, succes_register


urlpatterns = [
    # ----------------------------------------------------------------- #
    # ---------------------------- VISTAS ----------------------------- #
    # ----------------------------------------------------------------- #
    
    # WELCOME
    path('login/',login, name="login"),
    path('register/',register, name="register"),
    path('succesfull/',succes_register, name="succesfull"),
    
    
    # ----------------------------------------------------------------- #
    # ---------------------------- MÉTODOS ---------------------------- #
    # ----------------------------------------------------------------- #
    
    path('postCommerceRegistration/', postCommerceRegistration, name="postCommerceRegistration"),
]
