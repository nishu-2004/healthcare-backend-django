# mappings/serializers.py
from rest_framework import serializers
from .models import PatientDoctorMapping
# We'll import these later after migrations
# from patients.serializers import PatientListSerializer
# from doctors.serializers import DoctorListSerializer

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    # patient_details = PatientListSerializer(source='patient', read_only=True)
    # doctor_details = DoctorListSerializer(source='doctor', read_only=True)
    assigned_by_username = serializers.CharField(source='assigned_by.username', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = '__all__'
        read_only_fields = ('assigned_date', 'created_at', 'assigned_by')


class PatientDoctorMappingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ('patient', 'doctor', 'reason_for_assignment', 'is_active')


# Add the missing serializer
class PatientWithDoctorsSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    patient_name = serializers.CharField()
    doctors = serializers.ListField(child=serializers.DictField())