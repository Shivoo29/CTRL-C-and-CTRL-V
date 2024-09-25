from rest_framework import generics
from .models import TrafficLight
from .serializers import TrafficLightSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class TrafficLightListView(generics.ListAPIView):
    permission_classes =[IsAdminUser, IsAuthenticated]
    queryset = TrafficLight.objects.all()
    serializer_class = TrafficLightSerializer


class PresetConditionTrafficLightView(generics.ListAPIView):
    queryset = TrafficLight.objects.filter(preset_condition=True)
    serializer_class = TrafficLightSerializer

