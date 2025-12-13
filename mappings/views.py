from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor
from .serializers import (
    PatientDoctorMappingSerializer, 
    PatientDoctorMappingCreateSerializer,
    PatientWithDoctorsSerializer
)

class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can see mappings where they are the patient's owner or doctor's owner
        return PatientDoctorMapping.objects.filter(
            patient__user=self.request.user
        ) | PatientDoctorMapping.objects.filter(
            doctor__user=self.request.user
        )
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PatientDoctorMappingCreateSerializer
        return PatientDoctorMappingSerializer
    
    def perform_create(self, serializer):
        # Check if patient belongs to the user
        patient = serializer.validated_data['patient']
        if patient.user != self.request.user:
            raise serializers.ValidationError(
                {'error': 'You can only assign doctors to your own patients'}
            )
        
        # Check if mapping already exists
        if PatientDoctorMapping.objects.filter(
            patient=patient, 
            doctor=serializer.validated_data['doctor']
        ).exists():
            raise serializers.ValidationError(
                {'error': 'This doctor is already assigned to the patient'}
            )
        
        serializer.save(assigned_by=self.request.user)
    
    @action(detail=False, methods=['GET'], url_path='patient/(?P<patient_id>\d+)')
    def get_patient_doctors(self, request, patient_id=None):
        patient = get_object_or_404(Patient, id=patient_id)
        
        # Check if patient belongs to the user
        if patient.user != request.user:
            return Response(
                {'error': 'You can only view doctors for your own patients'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        mappings = PatientDoctorMapping.objects.filter(patient=patient, is_active=True)
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)


class PatientDoctorsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PatientDoctorMappingSerializer
    
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        patient = get_object_or_404(Patient, id=patient_id)
        
        # Check if patient belongs to the user
        if patient.user != self.request.user:
            return PatientDoctorMapping.objects.none()
        
        return PatientDoctorMapping.objects.filter(patient=patient, is_active=True)
