from django.urls import path
from .views import FileView, FileDownloadView

urlpatterns = [
    path('', FileView.as_view()),
    path('<str:name>', FileView.as_view()),
    path('download/<str:name>', FileDownloadView.as_view())
]