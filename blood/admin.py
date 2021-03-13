from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Location, Profile
# Register your models here.
admin.site.register(Location)
admin.site.register(Profile)
