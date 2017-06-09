from django.db import models
from django.contrib.auth.models import User

class City(models.Model):

    city = models.CharField(max_length=200, blank=False)
    office_adress = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return "{}".format(self.city)


class Trip(models.Model):

    start_time = models.DateField(null=True, blank=False)
    finish_time =  models.DateField(null=True, blank=False)
    departure = models.CharField(max_length=200, blank=False)
    arrival = models.ForeignKey(City, related_name='trips', on_delete=models.CASCADE, default=1)
    comfort = models.CharField(max_length=200, blank=False)
    hotel = models.CharField(max_length=200, blank=True)
    hotel_price = models.CharField(max_length=200, blank=True)
    hotel_stars = models.CharField(max_length=200, blank=True)
    flight = models.CharField(max_length=200, blank=True)
    flight_price = models.CharField(max_length=200, blank=True)
    departure_at = models.CharField(max_length=200, blank=True)
    return_at = models.CharField(max_length=200, blank=True)
    owner = models.ForeignKey('auth.User', related_name='owner', on_delete=models.CASCADE)


class Meeting (models.Model):
    
    trip = models.ForeignKey(Trip, related_name='meetings', on_delete=models.CASCADE)
    person = models.CharField(max_length=200, blank=False)
    date = models.DateField(null=True, blank=False)
    time = models.TimeField(null=True, blank=False)
    description = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    attendees = models.EmailField(blank=True)
    event_id = models.CharField(max_length=200, blank=True)

class UserProfile(models.Model):

    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=10)

