from django.urls import path
from task_manager.tasks import views


urlpatterns = [
    path('', views.TasksListView.as_view(), name='tasks_list'),
    path('create/', views.CreateTask.as_view(),
         name='task_create'),
    path('<int:pk>/update/', views.UpdateTask.as_view(),
         name='task_update'),
    path('<int:pk>/delete/', views.DeleteTask.as_view(),
         name='task_delete'),
    path('<int:pk>/', views.TaskDetailsView.as_view(),
         name='task_details'),
]
