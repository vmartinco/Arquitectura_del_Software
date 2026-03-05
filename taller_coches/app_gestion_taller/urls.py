from django.urls import path
from . import views

urlpatterns = [
    path('clientes', views.vista_cliente, name='cliente'),
    path('clientes/<int:cliente_id>/', views.detalle_cliente, name='detalle'),
]