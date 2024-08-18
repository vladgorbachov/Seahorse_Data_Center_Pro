from django.urls import path
from . import views

urlpatterns = [
    path('', views.catering_department, name='catering_department'),
    path('add_folder/', views.add_folder, name='catering_add_folder'),
    path('update_folder/<int:folder_id>/', views.update_folder, name='catering_update_folder'),
    path('delete_folder/<int:folder_id>/', views.delete_folder, name='catering_delete_folder'),
    path('get_max_folder_index/', views.get_max_folder_index, name='catering_get_max_folder_index'),
    path('table_view/<int:folder_id>/', views.table_view, name='catering_table_view'),
    path('save_table/', views.save_table, name='catering_save_table'),
    path('save_table_data/', views.save_table_data, name='catering_save_table_data'),
    path('delete_table_in_folder/<int:folder_id>/', views.delete_table_in_folder, name='catering_delete_table_in_folder'),
    path('folder/<int:folder_id>/', views.folder_view, name='catering_folder_view'),
    path('explorer/<int:folder_id>/', views.explorer_view, name='catering_explorer_view'),
    path('get_folder_contents/', views.get_folder_contents, name='catering_get_folder_contents'),
    path('file_action/', views.file_action, name='catering_file_action'),
    path('rename_file/', views.rename_file, name='catering_rename_file'),
    path('delete_file/', views.delete_file, name='catering_delete_file'),
    path('get_file_info/', views.get_file_info, name='catering_get_file_info'),
    path('pdf-viewer/', views.pdf_viewer, name='catering_pdf_viewer'),
]

