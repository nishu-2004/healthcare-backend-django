"""
URL configuration for healthcare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Authentication
    path('api/auth/', include('accounts.urls')),
    
    # Patient CRUD
    path('api/patients/', include('patients.urls')),
    
    # Doctor CRUD
    path('api/doctors/', include('doctors.urls')),
    
    # Mappings
    path('api/mappings/', include('mappings.urls')),
    
    # JWT Token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


# Access token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY1NjM5NjY2LCJpYXQiOjE3NjU2MzkzNjYsImp0aSI6IjI4OTNjYzNmZjkxOTQxMmE4MmJkNTViMGFmY2UwZmI2IiwidXNlcl9pZCI6IjIifQ.P-uHzxzr9Ts2o9-XhmGzhfrzJh_gNPspwwsBZedDoMU
