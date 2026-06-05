from rest_framework.views import APIView
from .models import Patient, PatientDoctorMapping
from .serializers import PatientSerializers, AssginDoctorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class PatientAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id, user):
        try:
            return Patient.objects.get(
                id=id,
                created_by=user
            )
        except Patient.DoesNotExist:
            return None
        
    def get(self, request, id=None):
        if id:
            patient = self.get_object(id, request.user)
            if not patient:
                return Response(
                    {
                        "error": "Patient not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = PatientSerializers(patient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        patients = Patient.objects.filter(created_by=request.user)
        serializer = PatientSerializers(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PatientSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(
                created_by = request.user
            )
            return Response(
                {
                    "message": "Patient created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        patient = self.get_object(id, request.user)
        if not patient:
            return Response(
                {
                    "error": "Patient not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PatientSerializers(patient, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Patient updated",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
        
    def delete(self, request, id):
        patient = self.get_object(id,request.user)
        if not patient:
            return Response(
                {
                    "error": "Patient not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        patient.delete()
        return Response(
            {
                "message": "Patient deleted "
            },
            status=status.HTTP_200_OK
        )

class MappingAPIView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        mappings = PatientDoctorMapping.objects.select_related("patient","doctor" )
        data = []
        for mapping in mappings:
            data.append({
                "id": mapping.id,
                "patient": mapping.patient.name,
                "doctor": mapping.doctor.name
            })
        return Response(data)

    def post(self, request):

        serializer = AssginDoctorSerializer(data=request.data)
        serializer.is_valid(
            raise_exception=True
        )
        mapping = PatientDoctorMapping.objects.create(
            patient_id=serializer.validated_data["patient_id"],
            doctor_id=serializer.validated_data["doctor_id"]
        )
        return Response(
            {
                "message": "Doctor assigned",
                "mapping_id": mapping.id
            },
            status=201
        )
class MappingDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        patient = get_object_or_404(Patient,id=patient_id)
        mappings = (PatientDoctorMapping.objects.filter(patient=patient).select_related("doctor"))
        doctors = []

        for mapping in mappings:
            doctors.append(
                {
                    "id": mapping.doctor.id,
                    "name": mapping.doctor.name
                }
            )
        return Response(
            {
                "patient": patient.name,
                "doctors": doctors
            }
        )
    def delete(self, request, patient_id):

        mapping = get_object_or_404(
            PatientDoctorMapping,
            id=patient_id
        )
        mapping.delete()
        return Response(
            {
                "message": "Mapping removed"
            }
        )