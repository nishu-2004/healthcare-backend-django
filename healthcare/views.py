# healthcare/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    RegisterSerializer, PatientSerializer, PatientListSerializer,
    DoctorSerializer, DoctorListSerializer, PatientDoctorMappingSerializer,
    PatientDoctorMappingCreateSerializer, PatientWithDoctorsSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly


# Authentication Views
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    from django.contrib.auth import authenticate
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Patient Views
class PatientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        return PatientSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['GET'])
    def doctors(self, request, pk=None):
        patient = self.get_object()
        mappings = PatientDoctorMapping.objects.filter(patient=patient, is_active=True)
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)


# Doctor Views
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DoctorListSerializer
        return DoctorSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['GET'])
    def patients(self, request, pk=None):
        doctor = self.get_object()
        mappings = PatientDoctorMapping.objects.filter(doctor=doctor, is_active=True)
        patients = [mapping.patient for mapping in mappings]
        serializer = PatientListSerializer(patients, many=True)
        return Response(serializer.data)


# Mapping Views
class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__user=self.request.user
        ) | PatientDoctorMapping.objects.filter(
            doctor__user=self.request.user
        )
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PatientDoctorMappingCreateSerializer
        return PatientDoctorMappingSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check if patient belongs to the user
            patient = serializer.validated_data['patient']
            if patient.user != request.user:
                return Response(
                    {'error': 'You can only assign doctors to your own patients'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if mapping already exists
            if PatientDoctorMapping.objects.filter(
                patient=patient, 
                doctor=serializer.validated_data['doctor']
            ).exists():
                return Response(
                    {'error': 'This doctor is already assigned to the patient'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Custom View for getting doctors of a specific patient
class PatientDoctorsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, patient_id):
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