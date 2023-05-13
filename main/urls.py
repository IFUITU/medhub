from django.urls import path, include
from .api_routes import router
from .views import PatientHistoryFilter

app_name = "main"

urlpatterns = [
    path("",include(router.urls)),
    # path("files-by-history/", PatientFileByPatientHistoryView.as_view(), name="files-by-history"),
    path("patient-history-filter/", PatientHistoryFilter.as_view(), name="patient-history-filter"),
]



