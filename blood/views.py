from django.shortcuts import render
from .models import Location, Profile
# Create your views here.
from math import sin, cos, sqrt, atan2, radians, degrees, sin, cos, radians, degrees, acos

# from django.contrib.gis.geos import Point


from geopy.distance import distance as geopy_distance

import requests

key = "b4ed70f1b29088efdaaac1f5d5e69873"

#twilio
from django.conf import settings                                                                                                                                                       
from django.http import HttpResponse
from twilio.rest import Client


def home(request):

    data = Location.objects.all()

    prof = Profile.objects.all()

    ls = []
    temp={}
    for x in prof:
        temp={}
        temp['name'] = x.name
        temp['contact'] = x.contact
        temp['address'] = x.address

        ip = x.ip

        url = "http://api.ipstack.com/" + ip +"?access_key=" + key
        response = requests.get(url).json()
        print(response)
        lat = response['latitude']
        lon = response['longitude']

        temp['latitude'] = lat
        temp['longitude'] = lon

        ls.append(temp)

    print(ls)
    return render(request, 'intro.html',{'data': ls} )

def search(request):

    user_lat = radians(19.1778797)
    user_lon = radians(72.8733183)

    data = Location.objects.all()

    R = 6373.0

    # lat1 = radians(52.2296756)
    # lon1 = radians(21.0122287)

    ls = []

    for x in data:
        lat_user = radians(19.1778797)
        lat_b = radians(x.latitude)
        long_diff = radians(72.8733183 - x.longitude)
        distance = (sin(lat_user) * sin(lat_b) +
                    cos(lat_user) * cos(lat_b) * cos(long_diff))
        resToMile = degrees(acos(distance)) * 69.09
        resToMt = resToMile / 0.00062137119223733

        print(resToMt)

        if resToMt < 31000:
            ls.append(x)

    # for x in data:

    #     lat2 = radians(x.latitude)
    #     lon2 = radians(x.longitude)

    #     dlon = lon2 - user_lon
    #     dlat = lat2 - user_lat

    #     a = sin(dlat / 2)**2 + cos(user_lat) * cos(lat2) * sin(dlon / 2)**2
    #     c = 2 * atan2(sqrt(a), sqrt(1 - a))

    #     distance = R * c

    #     if distance < 31:
    #         ls.append(x)
    # print(ls)
    # print("Result:", distance)
    # print("Should be:", 278.546, "km")

    # p1 = Point(19.1778797,72.8733183)

    # for x in data:

    #     p2 = Point(x.latitude, x.longitude)
    #     distance = p1.distance(p2)
    #     distance_in_km = distance * 100
    #     print(distance_in_km)


    return render(request, 'search.html',{'data': ls} )

def test(request):
    
    # if request.method == 'POST':
    print("hello")
    
    radius = 400000

    user_lat = radians(19.1778797)
    user_lon = radians(72.8733183)

    data = Profile.objects.all()

    R = 6373.0

    # lat1 = radians(52.2296756)
    # lon1 = radians(21.0122287)

    ls = []
    print(radius)
    for x in data:
        lat_user = radians(19.1778797)
        ip = x.ip
        key = "b4ed70f1b29088efdaaac1f5d5e69873"
        
        url = "http://api.ipstack.com/" + ip +"?access_key=" + key
        response = requests.get(url).json()
        print(response)
        lat = response['latitude']
        lon = response['longitude']

        lat_b = radians(lat)
        long_diff = radians(72.8733183 - lon)
        distance = (sin(lat_user) * sin(lat_b) +
                    cos(lat_user) * cos(lat_b) * cos(long_diff))
        resToMile = degrees(acos(distance)) * 69.09
        resToMt = resToMile / 0.00062137119223733

        print(resToMt)

        if resToMt < radius:
            temp={}
            temp['name'] = x.name
            temp['contact'] = x.contact
            temp['address'] = x.address

            ip = x.ip

            temp['latitude'] = lat
            temp['longitude'] = lon

            temp['id'] = x.id

            ls.append(temp)
                
    print(ls)

    return render(request, 'search.html', {'data': ls} )

def register(request):

    if request.method == "POST":
        name = request.POST['name']
        contact = request.POST['contact']
        address = request.POST['address']
        ip = request.POST['ip']
        print(name)
        print(ip)

           
        key = "b4ed70f1b29088efdaaac1f5d5e69873"
        
        url = "http://api.ipstack.com/" + ip +"?access_key=" + key
        response = requests.get(url).json()
        print(response)
        lat = response['latitude']
        lon = response['longitude']

        loc = Location.objects.create(latitude= lat, longitude=lon)

        Profile.objects.create(name = name, contact = contact, address = address, location=loc, ip = ip)

        return render(request, 'intro.html')
#http://api.ipstack.com/103.216.68.137?access_key=b4ed70f1b29088efdaaac1f5d5e69873
    return render(request, 'register.html')    


def sms(request):
    message_to_broadcast = ("Have you played the incredible TwilioQuest "
                                                "yet? Grab it here: https://www.twilio.com/quest")
    client = Client("AC9d8a94f846d748f362e6dda727e83eaa", "45c894517cded405080dcb9984c9ce27")
    for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
        if recipient:
            client.messages.create(to=recipient,
                                   from_="+14422426473",
                                   body=message_to_broadcast)
    return HttpResponse("messages sent!", 200)