from rest_framework import serializers
from .models import *
from django import forms

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'city', 'office_adress')

class TripSerializer(serializers.ModelSerializer):
    arrival = serializers.SlugRelatedField(many=False, queryset=City.objects.all(), slug_field='city')
    meetings = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    choices = (('0', 'More cheap'),
               ('1', 'More comfortable'))
    comfort = serializers.ChoiceField(choices)

    class Meta:
        model = Trip
        fields = ('id', 'start_time', 'finish_time', 'departure', 'arrival', 'comfort', 'meetings', 'hotel', 'hotel_price', 'hotel_stars', 'flight', 'flight_price', 'departure_at', 'return_at')
        read_only_fields = ('meetings', 'hotel', 'hotel_price', 'hotel_stars', 'flight', 'flight_price', 'flight_time', 'departure_at', 'return_at')

class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = ('trip', 'person', 'date', 'time', 'description', 'location', 'attendees', 'event_id')
        read_only_fields = ('trip', 'event_id')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        write_only_fields = ('password', )
        read_only_fields = ('id', )

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',  )
        write_only_fields = ('password', )
        read_only_fields = ('id', )