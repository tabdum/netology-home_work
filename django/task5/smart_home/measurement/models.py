from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)


class Sensor(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.PROTECT, related_name='measurements')
    temperature = models.FloatField()
    date_measured = models.DateTimeField(auto_now_add=True)
    image = models.URLField(blank=True, null=True)



