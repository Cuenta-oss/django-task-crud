from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.userRegister, name='register'),
    path('task/', views.taskView, name='task'),
    path('task_completed/', views.taskCompleted, name='task_completed'),
    path('logout/', views.logoutView, name='logout'),
    path('login/', views.singin, name='login'),
    path('create/', views.createTask, name='create'),
    path('task_detail/<int:task_id>/', views.taskDetail, name='task_detail'),
    path('task_edit/<int:task_id>/', views.taskEdit, name='task_edit'),
    path('task_edit/<int:task_id>/complete/', views.taskComplete, name='task_completed'),
    path('task_edit/<int:task_id>/delete/', views.taskDelete, name='task_delete'),
]