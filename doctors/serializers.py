from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Doctor

class DoctorSerializers(serializers.ModelSerializer):
    
    created_by = serializers.CharField(
    source='created_by.username',
    read_only=True
    )
    
    class Meta:
        model = Doctor
        fields = '__all__'

        extra_kwargs = {
            "name": {"required": True},
            "gender": {"required": True},
            "specialization": {"required": True},
            "experience": {"required": True},
            "phone": {"required": True}
        }

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
            "Phone number must contain only digit"
        )
        if len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must be exactly 10 digit"
            )

        return value
    
    def validate_experience(self, value):
       if value<=0:
            raise serializers.ValidationError(
                "Experience can't be negative"
            )
       return value