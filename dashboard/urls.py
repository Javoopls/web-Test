from . import views as main_views
from django.urls import path
from .views import index,login, register, mailling_collect, postNewCollect, apikeys, masive_mailling_collect,form_tecnico,negocio_historial,negocio_metricas,generar_y_mostrar_qr


urlpatterns = [
    # ----------------------------------------------------------------- #
    # ---------------------------- VISTAS ----------------------------- #
    # ----------------------------------------------------------------- #
    
    # WELCOME
    path('dashboard/',index, name="index"),
    path('login/',login, name="login"),
    path('register/',register, name="register"),
    path('apikeys/',apikeys, name="apikeys"),
    path('form_tecnico/',form_tecnico, name="form_tecnico"),
    path('negocio_historial/',negocio_historial, name="negocio_historial"),
    path('negocio_metricas/',negocio_metricas, name="negocio_metricas"),
    path('mailling_collect/',mailling_collect, name="mailling_collect"),
    path('masive_mailling_collect/',masive_mailling_collect, name="masive_mailling_collect"),
    path('generar_y_mostrar_qr/', generar_y_mostrar_qr, name='generar_y_mostrar_qr'),
    
    
    # ----------------------------------------------------------------- #
    # ---------------------------- MÉTODOS ---------------------------- #
    # ----------------------------------------------------------------- #
    path('postNewCollect/aaa/', postNewCollect, name="postNewCollect"),
    path('postGenerateApiKey/', main_views.postGenerateApiKey, name="postGenerateApiKey"),
    path('newApiKey/', main_views.newApiKey, name="newApiKey"),
    path('profile/', main_views.profile, name="profile"),
    path('blockdeprueba/', main_views.blockdeprueba, name="blockdeprueba"),
]
