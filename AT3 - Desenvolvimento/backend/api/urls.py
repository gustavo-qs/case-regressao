from api import views
from django.urls import path


urlpatterns = [
    path('usuarios/', views.usuario_list),
]