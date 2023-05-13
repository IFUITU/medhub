from django.urls import path
from .views import RegUserView, UserRetrieveView, ChangePassView, LogApi



app_name = "accounts"

urlpatterns = [
    path("", RegUserView.as_view(), name="register"),
    path("<int:pk>/", UserRetrieveView.as_view(), name="user-detail"),
    path("change-my-pass/", ChangePassView.as_view(), name="change-pass"),
    path("log/", LogApi.as_view(), name="user-log"),
]
