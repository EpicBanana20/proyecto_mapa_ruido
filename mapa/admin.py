from django.contrib import admin
from .models import Sensor, RegistroRuido

# Esto le dice a Django que muestre estas tablas en el panel
admin.site.register(Sensor)
admin.site.register(RegistroRuido)