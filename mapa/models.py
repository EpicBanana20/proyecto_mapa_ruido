from django.db import models
from django.utils import timezone

class Sensor(models.Model):
    nombre = models.CharField(max_length=100)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre

class RegistroRuido(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='registros')
    nivel_db = models.FloatField(help_text="Nivel de ruido en decibeles (dB)")
    fecha_hora = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"{self.sensor.nombre} - {self.nivel_db}dB a las {self.fecha_hora.strftime('%H:%M')}"