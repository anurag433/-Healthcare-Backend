from django.urls import path
from .views import DoctorAPIView

urlpatterns = [
    path('doctors/', DoctorAPIView.as_view()),
    path('doctors/<int:id>/',DoctorAPIView.as_view()),
]