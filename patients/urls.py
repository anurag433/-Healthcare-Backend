from django.urls import path
from .views import PatientAPIView, MappingAPIView , MappingDetailAPIView

urlpatterns = [
    path('patients/', PatientAPIView.as_view()),
    path('patients/<int:id>/',PatientAPIView.as_view()),
    path('mappings/',MappingAPIView.as_view()),
    path('mappings/<int:patient_id>/',MappingDetailAPIView.as_view())
]