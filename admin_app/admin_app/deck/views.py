from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Folder, Table, TableCell
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Max

def deck_department(request):
    folders = Folder.objects.filter(visible=True)
    return render(request, 'deck_department.html', {'folders': folders})

@csrf_exempt
def add_folder(request):
    if request.method == "POST":
        data = json.loads(request.body)
        existing_folder = Folder.objects.filter(name=data['name']).first()
        if existing_folder and existing_folder.link:
            return JsonResponse({'status': 'error', 'message': 'Link already exists'})

        folder = Folder(index=data['index'], name=data['name'], link=data.get('link', ''), visible=True)
        folder.save()
        return JsonResponse({'status': 'success', 'id': folder.id, 'message': 'Link added!'})

@csrf_exempt
def update_folder(request, folder_id):
    if request.method == "POST":
        data = json.loads(request.body)
        folder = Folder.objects.get(id=folder_id)
        folder.name = data.get('name', folder.name)
        folder.link = data.get('link', folder.link)
        folder.visible = data.get('visible', folder.visible)
        folder.save()
        return JsonResponse({'status': 'success'})

@csrf_exempt
def delete_folder(request, folder_id):
    if request.method == "POST":
        folder = Folder.objects.get(id=folder_id)
        folder.delete()
        return JsonResponse({'status': 'success'})

def folder_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    table = Table.objects.filter(folder=folder).first()
    rows = []
    if table:
        for row_number in range(table.rows):
            row = []
            for column_number in range(table.columns):
                cell = TableCell.objects.get(table=table, row=row_number, column=column_number)
                row.append(cell)
            rows.append({'cells': row})
    return render(request, 'folder_view.html', {'folder': folder, 'table': {'rows': rows} if table else None})

def table_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    table = Table.objects.filter(folder=folder).first()
    rows = []
    if table:
        for row_number in range(table.rows):
            row = []
            for column_number in range(table.columns):
                cell = TableCell.objects.get(table=table, row=row_number, column=column_number)
                row.append(cell)
            rows.append({'cells': row})
    return render(request, 'table_view.html', {'folder': folder, 'table': {'rows': rows} if table else None})

def get_max_folder_index(request):
    max_index = Folder.objects.aggregate(Max('index'))['index__max'] or 0
    return JsonResponse({'max_index': max_index})

@csrf_exempt
def save_table(request):
    if request.method == "POST":
        data = json.loads(request.body)
        folder_id = data['folder_id']
        rows = int(data['rows'])  # Преобразование строки в целое число
        columns = int(data['columns'])  # Преобразование строки в целое число
        folder = Folder.objects.get(id=folder_id)
        table = Table.objects.create(folder=folder, rows=rows, columns=columns)
        for row in range(rows):
            for column in range(columns):
                TableCell.objects.create(table=table, row=row, column=column, content="")
        return JsonResponse({'status': 'success', 'table_id': table.id})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def save_table_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_id = data['table_id']
        cells = data['cells']
        for cell in cells:
            table_cell = TableCell.objects.get(id=cell['id'])
            table_cell.content = cell['content']
            table_cell.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def delete_table(request, table_id):
    if request.method == "POST":
        table = get_object_or_404(Table, id=table_id)
        table.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

