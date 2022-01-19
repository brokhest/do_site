from django.urls import path
from . import views
from .views import UserLogin
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login', UserLogin.as_view(), name='login'),
    path('register',views.UserRegister.as_view(), name='register'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.TaskList.as_view(), name='tasks'),
    #path('user/<int:pk>', views.UserDetail.as_view(), name = 'user'),
    path('task/<int:pk>/', views.TaskDetail.as_view(), name='task'),
    path('task-update/<int:pk>/', views.TaskUpdate.as_view(), name='update'),
    path('task-delete/<int:pk>/', views.TaskDelete.as_view(), name='delete'),
    path('task/add', views.TaskAdd.as_view(), name='task_add'),

]