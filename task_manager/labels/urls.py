from django.urls import path
from task_manager.labels import views


urlpatterns = [
    path('', views.LabelsListView.as_view(),
         name='labels_list'),
    path('create/', views.CreateLabel.as_view(),
         name='label_create'),
    path('<int:pk>/update/', views.UpdateLabel.as_view(),
         name='label_update'),
    path('<int:pk>/delete/', views.DeleteLabel.as_view(),
         name='label_delete'),
]
