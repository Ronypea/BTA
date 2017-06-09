from django.conf.urls import url, include 
from rest_framework.urlpatterns import format_suffix_patterns 
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = { 
    url(r'^trip/$', NewTripView.as_view(), name="new-trip"), 
    url(r'^office/$', NewOfficeView.as_view(), name="new-office"),
    url(r'^trips/(?P<pk>[0-9]+)/$', TripDetailsView.as_view(), name="trip-details"),
    url(r'^trips/(?P<pk>[0-9]+)/meeting/$', NewMeetingView.as_view(), name="new-meeting"),
    url(r'^trips/(?P<trip_id>[0-9]+)/meetings/(?P<pk>[0-9]+)/$', MeetingDetailsView.as_view(), name="meeting-detail"),
    url(r'^delmeeting/(?P<pk>[0-9]+)/$', delmeeting, name="meeting-delete"),
    url(r'^trips/$', TripsView.as_view(), name="your-trips"), 
    url(r'^login/$', LoginView.as_view(), name="log-in"), 
    url(r'^logout/$', logout, name="log-out"),
    url(r'^registration/$', RegistrationView.as_view(), name="registration"), 
    url(r'^confirmation/$', confirmation, name="confirmation"),
    url(r'^activation/(?P<activation_key>[0-9]+)/$', activation, name="activation"), 
    url(r'^api-token-auth/', obtain_auth_token),
} 

urlpatterns = format_suffix_patterns(urlpatterns)
