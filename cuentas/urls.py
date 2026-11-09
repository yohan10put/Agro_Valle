from django.urls import path

from . import views

urlpatterns = [
    path('', views.portada, name='portada'),
    path('inicio/', views.inicio, name='inicio'),
    path('gestion/tecnicos/nuevo/', views.nuevo_tecnico, name='nuevo_tecnico'),
]
