from django.urls import path
from task_manager.task import views


urlpatterns = [
    path('', views.TasksListView.as_view(), name='tasks_list'),
    path('create/', views.CreateTask.as_view(),
         name='task_create'),
    path('<int:id>/update/', views.UpdateTask.as_view(),
         name='task_update'),
    path('<int:id>/delete/', views.DeleteTask.as_view(),
         name='task_delete'),
    path('<int:id>/', views.TaskDetailsView.as_view(),
         name='task_details'),
]
