# mappings/models.py
from django.db import models
from django.contrib.auth.models import User
from patients.models import Patient
from doctors.models import Doctor

class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_mappings')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_mappings')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assignments')
    assigned_date = models.DateField(auto_now_add=True)
    reason_for_assignment = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['patient', 'doctor']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.patient.first_name} {self.patient.last_name} - Dr. {self.doctor.first_name} {self.doctor.last_name}"