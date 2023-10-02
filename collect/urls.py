from . import views as main_views
from django.urls import path, include
from .views import index, verify, postVerifyUid, postNewCollect

urlpatterns = [
    # ================================================================= #
    # ---------------------------- VISTAS ----------------------------- #
    # ================================================================= #
    
    path('new/', index, name="index"),#<str:uid>
    path('verify/', verify, name="verify"),
    
    
    # ================================================================= #
    # ---------------------------- MÉTODOS ---------------------------- #
    # ================================================================= #
    
    # Formulario verificación ID
    path('verify/postVerifyUid/', postVerifyUid, name="postVerifyUid"),
    path('postNewCollect/<str:bid>', postNewCollect, name="postNewCollect"),
]