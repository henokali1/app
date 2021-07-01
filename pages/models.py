from django.utils import timezone
from datetime import datetime
from django.db import models

class EnergyLog(models.Model):
    current = models.FloatField(default=0.0)
    tot_enery = models.FloatField(default=0.0)
    set_voltage = models.FloatField(default=230.0)
    pwr = models.FloatField(default=0.0)
    date = models.DateTimeField(default=datetime.now)
    ts = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date) + ' - ' + str(self.tot_enery)

class EnvironmentalDataLog(models.Model):
    ts = models.IntegerField(default=0)
    temp  = models.FloatField(default=0.0)
    humidity  = models.FloatField(default=0.0)
    motion  = models.BooleanField(default=0)

    def __str__(self):
        return f'{self.ts} - Temp: {self.temp} - Humidity: {self.humidity} - Motion: {self.motion}'
