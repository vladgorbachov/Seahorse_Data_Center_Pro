from django.urls import path
from . import views

urlpatterns = [
    path('', views.electrical_department, name='electrical_department'),
    path('add_folder/', views.add_folder, name='electrical_add_folder'),
    path('update_folder/<int:folder_id>/', views.update_folder, name='electrical_update_folder'),
    path('delete_folder/<int:folder_id>/', views.delete_folder, name='electrical_delete_folder'),
    path('get_max_folder_index/', views.get_max_folder_index, name='electrical_get_max_folder_index'),
    path('table_view/<int:folder_id>/', views.table_view, name='electrical_table_view'),
    path('save_table/', views.save_table, name='electrical_save_table'),
    path('save_table_data/', views.save_table_data, name='electrical_save_table_data'),
    path('delete_table_in_folder/<int:folder_id>/', views.delete_table_in_folder, name='electrical_delete_table_in_folder'),
    path('folder/<int:folder_id>/', views.folder_view, name='electrical_folder_view'),
    path('explorer/<int:folder_id>/', views.explorer_view, name='electrical_explorer_view'),
    path('get_folder_contents/', views.get_folder_contents, name='electrical_get_folder_contents'),
    path('file_action/', views.file_action, name='electrical_file_action'),
    path('rename_file/', views.rename_file, name='electrical_rename_file'),
    path('delete_file/', views.delete_file, name='electrical_delete_file'),
    path('get_file_info/', views.get_file_info, name='electrical_get_file_info'),
    path('pdf-viewer/', views.pdf_viewer, name='electrical_pdf_viewer'),
]

