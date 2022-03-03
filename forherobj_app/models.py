from django.db import models
from django.contrib.auth.models import User


class WeatherDetails(models.Model):

    city_name = models.CharField(max_length=120)
    longitude = models.CharField(max_length=30)
    latitude = models.CharField(max_length=30)
    temperature = models.CharField(max_length=10)
    country = models.CharField(max_length=5)
    weather_type = models.CharField(max_length=20)
    icon = models.CharField(max_length=5)

    user_requested = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.city_name, self.temperature)