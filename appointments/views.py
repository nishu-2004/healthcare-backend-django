from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    # For dynamic viewing
    def querysat(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        doctor = params.get("doctor")
        patient = params.get("patient")
        status = params.get("status")

        if doctor:
            queryset = queryset.filter(doctor_id = doctor)
        if patient:
            queryset = queryset.filter(doctor_id = doctor)
        if status:
            queryset = queryset.filter(doctor_id = doctor)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)