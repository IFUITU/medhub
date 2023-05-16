from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from .models import PatientFile, PatientHistory
from .filters import PatientHistoryFilter
from .permissions import IsDoctor, IsPatientsDoctor, IsDoctorForFile
from .serializers import (
    PatientHistorySerializer, PatientFileCreateSerializer, 
    PatientFileSerializer, GroupedPatientInfoSerializer
)


class PatientHistoryViewSet(ModelViewSet):
    serializer_class = PatientHistorySerializer
    queryset = PatientHistory.objects.all()
    permission_classes = [IsPatientsDoctor]

    def get_serializer_class(self):
        if self.action == "list":
            return GroupedPatientInfoSerializer
        return PatientHistorySerializer

    def get_queryset(self):
        if self.action == "list":
            queryset = PatientFile.objects.all()

            grouped_by_history = {}
            for file in queryset:
                patinet_history = file.patient_history
                if patinet_history in grouped_by_history:
                    grouped_by_history[patinet_history]['patient_files'].append(file)
                else:
                    grouped_by_history[patinet_history] = {
                        'patient_history':patinet_history,
                        'patient_files':[file]}
            return grouped_by_history.values()
        return super().get_queryset()


class PatientFileViewset(ModelViewSet):
    serializer_class = PatientFileSerializer
    queryset = PatientFile.objects.all()
    permission_classes = [IsDoctorForFile]

    def get_serializer_class(self):
        if self.action == "create":
            return PatientFileCreateSerializer
        return PatientFileSerializer


#Patient History Filters
class PatientHistoryFilter(ListAPIView):
    queryset = PatientHistory.objects.all()
    serializer_class = PatientHistorySerializer
    permission_classes = [IsDoctor]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = PatientHistoryFilter
    filterset_fields = ['patient_name', "patient_birth_date", "patient_med_condition"]
    search_fields = ['patient_name', 'patient_birth_date', 'patient_med_condition']
