from rest_framework import routers
from .views import PatientHistoryViewSet, PatientFileViewset

router = routers.DefaultRouter()
router.register('patient-history', PatientHistoryViewSet, basename="patient-history")
router.register('patient-file', PatientFileViewset, basename="patient-file")