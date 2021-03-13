from django.db import models
from django.contrib.auth.models import User, auth
# Create your models here.


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

class Profile(models.Model):
    name = models.CharField(max_length=50)
    contact = models.IntegerField()
    address = models.CharField(max_length=200) 
    location = models.OneToOneField(Location, on_delete=models.CASCADE)  
    ip = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    bloodgroup = models.CharField(max_length=2, default="O+")

