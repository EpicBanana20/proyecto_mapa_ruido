import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# 1. Conectamos este script con la configuración de tu proyecto Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config_ruido.settings')
django.setup()

# 2. Importamos tus modelos
from mapa.models import Sensor, RegistroRuido

def poblar_datos():
    sensores = Sensor.objects.all()
    if not sensores:
        print("No hay sensores en la base de datos. Agrega al menos uno en el panel de admin.")
        return

    print(f"Generando historial de 10 días para {sensores.count()} sensores...")
    
    ahora = timezone.now()
    registros_a_crear = []

    for sensor in sensores:
        # Borramos el historial viejo de este sensor para no duplicar si corres el script varias veces
        sensor.registros.all().delete()

        # Viajamos 10 días al pasado y vamos avanzando hasta la hora actual
        for dias_atras in range(10, -1, -1): 
            # Generamos una lectura cada 2 horas para tener una gráfica detallada
            for hora in range(0, 24, 2): 
                fecha_lectura = ahora - timedelta(days=dias_atras)
                fecha_lectura = fecha_lectura.replace(hour=hora, minute=random.randint(0, 59))
                
                # Evitamos crear registros en el futuro (si hoy es el día 0 y la hora aún no pasa)
                if fecha_lectura > ahora:
                    continue

                # Simulamos la realidad: los días son más ruidosos que las madrugadas
                if 8 <= hora <= 20:
                    ruido = random.uniform(65.0, 95.0) # Tráfico, gente, construcciones
                else:
                    ruido = random.uniform(35.0, 55.0) # Noche tranquila

                registros_a_crear.append(
                    RegistroRuido(
                        sensor=sensor,
                        nivel_db=round(ruido, 1),
                        fecha_hora=fecha_lectura
                    )
                )

    # Guardamos todos los registros en la base de datos de un solo golpe (es mucho más rápido)
    RegistroRuido.objects.bulk_create(registros_a_crear)
    print(f"¡Éxito! Se generaron {len(registros_a_crear)} registros de ruido ambiental.")

if __name__ == '__main__':
    poblar_datos()