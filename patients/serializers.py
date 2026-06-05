from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient, PatientDoctorMapping
from doctors.models import Doctor

class PatientSerializers(serializers.ModelSerializer):

    created_by = serializers.CharField(
    source='created_by.username',
    read_only=True
    )
    
    class Meta:
        model = Patient
        fields = '__all__'

        extra_kwargs = {
            "name": {"required": True},
            "age": {"required": True},
            "gender": {"required": True},
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
    
    def validate_age(self, value):
       if value<=0:
            raise serializers.ValidationError(
                "Age must be greater than 0"
            )
       return value
    

class AssginDoctorSerializer(serializers.Serializer):
    
    patient_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField()

    def validate_patient_id(self, value):
        if not Patient.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "Patient not exist"
            )
        return value
    
    def validate_doctor_id(self, value):
        if not Doctor.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "Doctor not exist"
            )
        return value
    
    def validate(self, attrs):
        if PatientDoctorMapping.objects.filter(
            patient_id=attrs["patient_id"],
            doctor_id=attrs["doctor_id"]
        ).exists():
            raise serializers.ValidationError(
                "Mapping already exists"
            )

        return attrs