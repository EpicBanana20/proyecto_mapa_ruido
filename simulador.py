import os
import django
import time
import random
from django.utils import timezone

# Conectamos con tu proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config_ruido.settings')
django.setup()

from mapa.models import Sensor, RegistroRuido

def iniciar_simulacion():
    print("Iniciando simulador de sensores... (Presiona Ctrl+C para detener)")
    
    while True: # Este ciclo infinito mantendrá el script corriendo
        sensores = Sensor.objects.all()
        hora_actual = timezone.now().strftime('%H:%M:%S')
        
        for sensor in sensores:
            # Inventamos un nivel de ruido aleatorio entre 40 y 85 dB
            ruido = round(random.uniform(40.0, 85.0), 1)
            
            # Lo guardamos en la base de datos
            RegistroRuido.objects.create(
                sensor=sensor, 
                nivel_db=ruido, 
                fecha_hora=timezone.now()
            )
            print(f"[{hora_actual}] Nuevo registro en {sensor.nombre}: {ruido} dB")
            
        # El script "se duerme" 60 segundos antes de volver a empezar
        time.sleep(10) 

if __name__ == '__main__':
    iniciar_simulacion()