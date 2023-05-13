from rest_framework.viewsets import ModelViewSet

from .serializers import PatientHistorySerializer, PatientFileCreateSerializer, PatientFileSerializer
from .models import PatientFile, PatientHistory

class PatientHistoryViewSet(ModelViewSet):
    serializer_class = PatientHistorySerializer
    queryset = PatientHistory.objects.all()


class PatientFileViewset(ModelViewSet):
    serializer_class = PatientFileSerializer
    queryset = PatientFile.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return PatientFileCreateSerializer
        return PatientFileSerializer