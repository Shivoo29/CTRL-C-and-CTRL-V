from django.urls import path,include
from .views import *

urlpatterns = [
    path('', TrafficLightListView.as_view(), name='all-traffic-lights'),
    path('traffic-lights/preset/', PresetConditionTrafficLightView.as_view(), name='preset-traffic-lights'),
]
