from django.urls import path
from . import views

urlpatterns = [
    path('', views.deck_department, name='deck_department'),
    path('add_folder/', views.add_folder, name='add_folder'),
    path('update_folder/<int:folder_id>/', views.update_folder, name='update_folder'),
    path('delete_folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('folder/<int:folder_id>/', views.folder_view, name='folder_view'),  # Новый маршрут
    path('get_max_folder_index/', views.get_max_folder_index, name='get_max_folder_index'),
]
