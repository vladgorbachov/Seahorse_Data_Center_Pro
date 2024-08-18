from django.urls import path
from . import views

urlpatterns = [
    path('', views.bridge_department, name='bridge_department'),
    path('add_folder/', views.add_folder, name='bridge_add_folder'),
    path('update_folder/<int:folder_id>/', views.update_folder, name='bridge_update_folder'),
    path('delete_folder/<int:folder_id>/', views.delete_folder, name='bridge_delete_folder'),
    path('get_max_folder_index/', views.get_max_folder_index, name='bridge_get_max_folder_index'),
    path('table_view/<int:folder_id>/', views.table_view, name='bridge_table_view'),
    path('save_table/', views.save_table, name='bridge_save_table'),
    path('save_table_data/', views.save_table_data, name='bridge_save_table_data'),
    path('delete_table_in_folder/<int:folder_id>/', views.delete_table_in_folder, name='bridge_delete_table_in_folder'),
    path('folder/<int:folder_id>/', views.folder_view, name='bridge_folder_view'),
    path('explorer/<int:folder_id>/', views.explorer_view, name='bridge_explorer_view'),
    path('get_folder_contents/', views.get_folder_contents, name='bridge_get_folder_contents'),
    path('file_action/', views.file_action, name='bridge_file_action'),
    path('rename_file/', views.rename_file, name='bridge_rename_file'),
    path('delete_file/', views.delete_file, name='bridge_delete_file'),
    path('get_file_info/', views.get_file_info, name='bridge_get_file_info'),
    path('pdf-viewer/', views.pdf_viewer, name='bridge_pdf_viewer'),
    path('dp_days_calendar/', views.dp_days_calendar, name='dp_days_calendar'),
    path('get_dp_hours/', views.get_dp_hours, name='get_dp_hours'),
    path('save_dp_hours/', views.save_dp_hours, name='save_dp_hours'),
]

