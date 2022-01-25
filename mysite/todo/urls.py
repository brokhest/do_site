from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, Tasks, GetTask

urlpatterns = [
    path('register/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('task_list/', Tasks.as_view()),
    path('task_list/<int:pk>', Tasks.as_view()),
    path('task_get/<int:pk>', GetTask.as_view()),
]