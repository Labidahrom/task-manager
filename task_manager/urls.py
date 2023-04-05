from django.contrib import admin
from django.urls import path
from task_manager import views


urlpatterns = [
    path('', views.index, name='index'),
    path('users/create/', views.CreateUser.as_view(), name='user_create'),
    path('users/<int:id>/update/', views.UpdateUser.as_view(), name='user_update'),
    path('users/<int:id>/delete/', views.DeleteUser.as_view(), name='user_delete'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('users/', views.UsersListView.as_view(), name='users_list'),
    path('admin/', admin.site.urls),
    path('statuses/', views.StatusesListView.as_view(), name='statuses_list'),
    path('statuses/create/', views.CreateStatus.as_view(), name='status_create'),
    path('statuses/<int:id>/update/', views.UpdateStatus.as_view(), name='status_update'),
    path('statuses/<int:id>/delete/', views.DeleteStatus.as_view(), name='status_delete'),
]
