from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientDoctorMappingViewSet, PatientDoctorsView

router = DefaultRouter()
router.register(r'', PatientDoctorMappingViewSet, basename='mapping')

urlpatterns = [
    path('', include(router.urls)),
    path('patient/<int:patient_id>/', PatientDoctorsView.as_view(), name='patient-doctors'),
]