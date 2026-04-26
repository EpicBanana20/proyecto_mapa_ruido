from django.shortcuts import render
from django.http import JsonResponse
from .models import Sensor

def mapa_principal(request):
    return render(request, 'mapa/index.html')

def datos_sensores(request):
    sensores = Sensor.objects.all()
    datos = []
    
    for sensor in sensores:
        ultima_lectura = sensor.registros.first() 
        nivel_actual = ultima_lectura.nivel_db if ultima_lectura else 0
        hora_actual = ultima_lectura.fecha_hora.strftime('%H:%M') if ultima_lectura else "Sin datos"

        datos.append({
            'id': sensor.id,
            'nombre': sensor.nombre,
            'lat': sensor.latitud,
            'lng': sensor.longitud,
            'db_actual': nivel_actual,
            'hora': hora_actual
        })
        
    return JsonResponse(datos, safe=False)

def historial_sensor(request, sensor_id):
    sensor = Sensor.objects.get(id=sensor_id)
    
    # Tomamos las últimas 24 lecturas (las más recientes)
    ultimos_registros = sensor.registros.all()[:24] 
    
    # Las invertimos para que en la gráfica aparezcan de la más vieja a la más nueva (de izquierda a derecha)
    registros_ordenados = list(ultimos_registros)[::-1]
    
    # En lugar de solo la hora, mandamos "Día Hora" para que se entienda mejor en la gráfica
    etiquetas = [r.fecha_hora.strftime('%d/%m %H:%M') for r in registros_ordenados]
    niveles = [r.nivel_db for r in registros_ordenados]
    
    return JsonResponse({
        'etiquetas': etiquetas,
        'niveles': niveles
    })