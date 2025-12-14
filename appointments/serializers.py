from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ["created_by"]

    def validate(self, data):
        doctor = data.get("doctor")
        appointment_datetime = data.get("appointment_datetime")

        if self.instance is None:  # CREATE only
            conflict = Appointment.objects.filter(
                doctor=doctor,
                appointment_datetime=appointment_datetime,
                status="SCHEDULED"
            ).exists()

            if conflict:
                raise serializers.ValidationError(
                    "Doctor already has an appointment at this time."
                )

        return data
