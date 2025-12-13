# doctors/models.py
from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('GP', 'General Practitioner'),
        ('CAR', 'Cardiologist'),
        ('NEU', 'Neurologist'),
        ('PED', 'Pediatrician'),
        ('ORTH', 'Orthopedist'),
        ('DERM', 'Dermatologist'),
        ('PSY', 'Psychiatrist'),
        ('RAD', 'Radiologist'),
        ('SUR', 'Surgeon'),
        ('OTH', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    hospital = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"