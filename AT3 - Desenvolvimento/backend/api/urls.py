from api import views
from django.urls import path


urlpatterns = [
    # autenticação
    path('login/',  views.login_view,  name='login'),
    path('logout/', views.logout_view, name='logout'),

    # rotas protegidas
    path('usuarios/',            views.users),
    path('prever/',              views.predict),
    path('previsoes/',           views.predictions),
    path('previsoes/<int:id>/',  views.predictions_delete),
]