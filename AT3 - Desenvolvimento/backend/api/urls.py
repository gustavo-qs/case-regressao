from api import views
from django.urls import path


urlpatterns = [
    path('usuarios/', views.users),
    path('prever/', views.predict),
    path('previsoes/', views.predictions),
    path('previsoes/<int:id>/', views.predictions_delete)
]