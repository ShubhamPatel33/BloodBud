from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('search', views.search, name="search"),
   
    path('register', views.register, name="register"),
    path('sms', views.sms, name="sms"),
    path('login', views.login, name="login"),
    path('mydata', views.mydata, name="mydata"),
    path('emergency', views.emergency, name="emergency"),    
    
]