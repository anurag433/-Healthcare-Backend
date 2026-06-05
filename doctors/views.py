from rest_framework.views import APIView
from .models import Doctor
from .serializers import DoctorSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class DoctorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id, user):
        try:
            return Doctor.objects.get(
                id=id,
                created_by=user
            )
        except Doctor.DoesNotExist:
            return None
        
    def get(self, request, id=None):
        if id:
            doctor = self.get_object(id, request.user)
            if not doctor:
                return Response(
                    {
                        "error": "Doctor not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = DoctorSerializers(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        doctors = Doctor.objects.all()
        serializer = DoctorSerializers(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DoctorSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(
                created_by = request.user
            )
            return Response(
                {
                    "message": "Doctor created",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id):
        doctor = self.get_object(id, request.user)
        if not doctor:
            return Response(
                {
                    "error": "Doctor not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = DoctorSerializers(doctor, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Doctor updated",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
    def delete(self, request, id):
        doctor = self.get_object(id,request.user)
        if not doctor:
            return Response(
                {
                    "error": "Doctor not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        doctor.delete()
        return Response(
            {
                "message": "Doctor deleted "
            },
            status=status.HTTP_200_OK
        )