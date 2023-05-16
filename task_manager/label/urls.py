from django.urls import path
from task_manager.label import views


urlpatterns = [
    path('', views.LabelsListView.as_view(),
         name='labels_list'),
    path('create/', views.CreateLabel.as_view(),
         name='label_create'),
    path('<int:id>/update/', views.UpdateLabel.as_view(),
         name='label_update'),
    path('<int:id>/delete/', views.DeleteLabel.as_view(),
         name='label_delete'),
]
