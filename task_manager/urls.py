from django.contrib import admin
from django.urls import path, include
from task_manager import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('users/', include('task_manager.user.urls')),
    path('statuses/', include('task_manager.status.urls')),
    path('tasks/', include('task_manager.task.urls')),
    path('labels/', include('task_manager.label.urls')),
]
