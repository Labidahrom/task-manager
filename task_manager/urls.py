from django.contrib import admin
from django.urls import path, include
from task_manager import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('users/', include('task_manager.user.urls')),
    path('admin/', admin.site.urls),
    path('statuses/', include('task_manager.status.urls')),
    path('tasks/', views.TasksListView.as_view(), name='tasks_list'),
    path('tasks/create/', views.CreateTask.as_view(),
         name='task_create'),
    path('tasks/<int:id>/update/', views.UpdateTask.as_view(),
         name='task_update'),
    path('tasks/<int:id>/delete/', views.DeleteTask.as_view(),
         name='task_delete'),
    path('tasks/<int:id>/', views.TaskDetailsView.as_view(),
         name='task_details'),
    path('labels/', include('task_manager.label.urls')),
]
