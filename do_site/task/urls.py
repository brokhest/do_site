from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.Task_list.as_view(), name='list'),
    path('<int:pk>', views.Task_list.as_view(), name="update"),
    re_path('registration', views.RegistrationAPIView.as_view(), name='user_registration'),
    re_path('login', views.LoginAPIView.as_view(), name='login'),

]