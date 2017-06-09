from django.shortcuts import render, get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django import forms
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.views import APIView
from django.core.mail import send_mail
from .serializers import * 
from .models import *
from . import Hotellook
from . import Aviasales
from . import Google_Calendar
import requests
import random

class NewOfficeView(generics.ListCreateAPIView):
    serializer_class = CitySerializer
    renderer_classes = (TemplateHTMLRenderer, )
    template_name='newoffice.html'

    def get(self, request, *args, **kwargs):
        return Response({'serializer': CitySerializer, 'username': request.session['Username']})

    def post(self, request):
        c = City(city = request.data['city'], office_adress=request.data['office_adress'])
        c.save()
        return Response({'serializer': CitySerializer, 'username': request.session['Username']})

class NewTripView(generics.ListCreateAPIView):
    serializer_class = TripSerializer
    renderer_classes = (TemplateHTMLRenderer, )
    template_name='newtrip.html'

    def get(self, request, *args, **kwargs):
        return Response({'serializer': TripSerializer, 'username': request.session['Username']})

    def post(self, request, *args, **kwargs):
        a = City.objects.filter(city=request.data['arrival'])[0]
        for u in User.objects.all():
            if u.username == request.session['Username']:
                user = u
        t = Trip(start_time=request.data['start_time'], finish_time=request.data['finish_time'], departure=request.data['departure'], arrival=a, comfort = request.data['comfort'], owner=user)
        t.save()
        adress = a.office_adress
        resp = {'time_dep': str(request.data['start_time']), 'time_ar': str(request.data['finish_time']), 'departure': request.data['departure'], 'arrival': a.city, 'status': int(request.data['comfort']), 'adress': adress}
        hotel = Hotellook.start(resp)
        t.hotel = hotel['data'][0]['hotelName']
        t.hotel_price = hotel['data'][0]['priceAvg']
        t.hotel_stars = hotel['data'][0]['stars']
        ticket = Aviasales.start(resp)
        t.flight = ticket['airline'] + str(ticket['flight_number'])
        t.flight_price = ticket['price']
        t.departure_at = ticket['departure_at'].replace('T', '   ').replace('Z', '')[:-3]
        t.return_at = ticket['return_at'].replace('T', '   ').replace('Z', '')[:-3]
        t.save()
        return Response({'serializer': TripSerializer, 'username': request.session['Username']})

class TripDetailsView(APIView):
    renderer_classes = (TemplateHTMLRenderer, )
    template_name = 'tripdetails.html'

    def get(self, request, *args, **kwargs):
        idx = self.kwargs.get('pk', None)
        trip = Trip.objects.get(id=idx)
        meetings = Meeting.objects.filter(trip_id=idx)
        return Response({'username': request.session['Username'], 'trip': trip, 'meetings': meetings})

    def post(self, request, pk):
        for m in Meeting.objects.filter(trip_id=pk):
            m.delete()
        Trip.objects.get(id=pk).delete()
        return HttpResponseRedirect('http://127.0.0.1:8000/trips/')


class TripsView(APIView):
    renderer_classes = (TemplateHTMLRenderer, )
    template_name = 'trips.html'
    queryset = Trip.objects.all()

    def get(self, request):
        for u in User.objects.all():
            if u.username == request.session['Username']:
                idx = u.id
        trips = Trip.objects.filter(owner=idx)
        return Response({'trips': trips, 'username': request.session['Username']})

class NewMeetingView(generics.ListCreateAPIView):
    serializer_class = MeetingSerializer
    renderer_classes = (TemplateHTMLRenderer, )
    template_name='newmeeting.html'

    def get(self, request, pk):
        return Response({'serializer': MeetingSerializer, 'pk': pk, 'username': request.session['Username']})

    def post(self, request, pk):
        trip = Trip.objects.get(id=pk)
        m = Meeting(trip = trip, person=request.data['person'], date=request.data['date'], time=request.data['time'],
                    description=request.data['description'], location=request.data['location'],
                    attendees=request.data['attendees'])
        m.save()
        resp = {'summary': 'Meeting with {}'.format(request.data['person']),
                'start': {'dateTime': str(request.data['date']) + 'T' + str(request.data['time']) + ':00Z'},
                'end': {'dateTime': str(request.data['date']) + 'T' + str(request.data['time']) + ':00Z'},
                'location': request.data['location'],
                'description': request.data['description'],
                'attendees': [
                    {'email': request.data['attendees'],}
                    ],
                'id': '',
                'meeting_id': m.id
                }
        if resp['attendees'][0]['email'] == '':
            resp.pop('attendees')
        Google_Calendar.start('create', resp)
        return Response({'serializer': MeetingSerializer, 'pk': pk, 'username': request.session['Username']})

class MeetingDetailsView(generics.ListCreateAPIView):
    serializer_class = MeetingSerializer
    renderer_classes = (TemplateHTMLRenderer, )
    template_name='meetingdetails.html'

    def get(self, request, trip_id, pk):
        m = Meeting.objects.get(pk=pk)
        return Response({'serializer': MeetingSerializer, 'meeting': m, 'username': request.session['Username']})

    def post(self, request, trip_id, pk):
        m = Meeting.objects.get(pk=pk)
        m.person=request.data['person']
        m.date=request.data['date']
        m.time=request.data['time']
        m.description=request.data['description']
        m.location=request.data['location']
        m.attendees=request.data['attendees']
        m.save()
        return Response({'serializer': MeetingSerializer, 'meeting': m, 'username': request.session['Username']})

def delmeeting(request, pk):
    m = Meeting.objects.get(pk=pk)
    Google_Calendar.start('delete', {'id': m.event_id, 'meeting_id': ''})
    Meeting.objects.get(pk=pk).delete()
    return HttpResponseRedirect('http://127.0.0.1:8000/trips/')

class LoginView(APIView):
    renderer_classes = (TemplateHTMLRenderer, )
    template_name = 'login.html'
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({'serializer': UserSerializer})

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        data = dict(username=username, password=password)
        response = requests.post('http://127.0.0.1:8000/api-token-auth/', data)
        if response.status_code == 200:
            request.session['Authorization'] = 'Token ' + response.json()['token']
            request.session['Username'] = username
            requests.Session().headers = dict(Authorization=request.session['Authorization'])
            return HttpResponseRedirect('http://127.0.0.1:8000/trip/')
        else:
            text = 'Sorry, wrong username or password'
            return Response({'serializer': UserSerializer, 'text': text})


class RegistrationView(APIView):
    renderer_classes = (TemplateHTMLRenderer, )
    template_name = 'registration.html'
    serializer_class = UserRegistrationSerializer

    def get(self, request, *args, **kwargs):
        return Response({'serializer': UserRegistrationSerializer})

    def post(self, request):
        activation_key=str(random.randint(10**9, 10**10-1))
        email=request.data['email']
        user = User.objects.create(
            username=request.data['username'],
            email=email,
            is_active=False,
        )
        t = Token.objects.create(user=user)
        user.set_password(request.data['password'])
        user.save()
        new_profile = UserProfile(user=user, activation_key=activation_key)
        new_profile.save()
        email_subject = 'Confirmation'
        email_body = 'Hey! Follow this link: http://127.0.0.1:8000/activate/{}'.format(activation_key)
        send_mail(email_subject, email_body, 'prikladnaya16@yandex.ru', [email], fail_silently=False)
        return HttpResponseRedirect('http://127.0.0.1:8000/confirmation/')


def confirmation(request):
    return render(request, 'confirmation.html')

def activation(request, activation_key):
    idx = get_object_or_404(UserProfile, activation_key=activation_key)
    u = User.objects.get(id=idx.user_id)
    u.is_active = True
    u.save()
    return render(request, 'activation.html')

def logout(request):
    request.session.pop('Authorization')
    request.session.pop('Username')
    return HttpResponseRedirect('http://127.0.0.1:8000/login/')
