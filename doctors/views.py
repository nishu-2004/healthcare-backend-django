from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Doctor
from .serializers import DoctorSerializer, DoctorListSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # All authenticated users can view all doctors
        return Doctor.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DoctorListSerializer
        return DoctorSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if the doctor belongs to the current user
        if instance.user != request.user:
            return Response(
                {'error': 'You can only update doctors you created.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if the doctor belongs to the current user
        if instance.user != request.user:
            return Response(
                {'error': 'You can only delete doctors you created.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)