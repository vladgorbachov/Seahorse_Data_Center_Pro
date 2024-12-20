from django.urls import path
from . import views

urlpatterns = [
    path('', views.deck_department, name='deck_department'),
    path('add_folder/', views.add_folder, name='add_folder'),
    path('update_folder/<int:folder_id>/', views.update_folder, name='update_folder'),
    path('delete_folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('get_max_folder_index/', views.get_max_folder_index, name='get_max_folder_index'),
    path('table_view/<int:folder_id>/', views.table_view, name='table_view'),
    path('save_table/', views.save_table, name='save_table'),
    path('save_table_data/', views.save_table_data, name='save_table_data'),
    path('delete_table_in_folder/<int:folder_id>/', views.delete_table_in_folder, name='delete_table_in_folder'),
    path('folder/<int:folder_id>/', views.folder_view, name='folder_view'),
    path('explorer/<int:folder_id>/', views.explorer_view, name='explorer_view'),
    path('get_folder_contents/', views.get_folder_contents, name='get_folder_contents'),
    path('file_action/', views.file_action, name='file_action'),
    path('rename_file/', views.rename_file, name='rename_file'),
    path('delete_file/', views.delete_file, name='delete_file'),
    path('get_file_info/', views.get_file_info, name='get_file_info'),
    path('pdf-viewer/', views.pdf_viewer, name='pdf_viewer'),
]
