from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
