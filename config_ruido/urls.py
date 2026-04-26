from django.contrib import admin
from django.urls import path
from mapa import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mapa_principal, name='mapa_principal'),
    path('api/sensores/', views.datos_sensores, name='datos_sensores'),
    path('api/sensores/<int:sensor_id>/historial/', views.historial_sensor, name='historial_sensor'),
]