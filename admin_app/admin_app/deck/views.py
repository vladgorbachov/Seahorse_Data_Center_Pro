from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse
from .models import Folder, Table, TableCell, FileMetadata
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Max
import os
import mimetypes
from datetime import datetime


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

        link = data.get('link', '')
        link = link.replace('\\', '/')
        is_local_link = ':/' in link

        if is_local_link:
            link = 'file://' + link.replace('\\', '/')

        folder = Folder(index=data['index'], name=data['name'], link=link, is_local_link=is_local_link, visible=True)
        folder.save()
        return JsonResponse({'status': 'success', 'id': folder.id, 'link': folder.link, 'message': 'Link added!'})


@csrf_exempt
def update_folder(request, folder_id):
    if request.method == "POST":
        data = json.loads(request.body)
        folder = Folder.objects.get(id=folder_id)
        folder.name = data.get('name', folder.name)

        link = data.get('link', folder.link)
        link = link.replace('\\', '/')
        is_local_link = ':/' in link

        if is_local_link:
            link = 'file://' + link.replace('\\', '/')

        folder.link = link
        folder.is_local_link = is_local_link
        folder.visible = data.get('visible', folder.visible)
        folder.save()
        return JsonResponse({'status': 'success', 'link': folder.link})


@csrf_exempt
def delete_folder(request, folder_id):
    if request.method == "POST":
        folder = Folder.objects.get(id=folder_id)
        folder.delete()
        return JsonResponse({'status': 'success'})


def folder_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    if folder.is_local_link:
        return explorer_view(request, folder_id)

    table = Table.objects.filter(folder=folder).select_related('folder').first()
    rows = []
    table_id = None
    if table:
        table_id = table.id
        for row_number in range(table.rows):
            row = []
            for column_number in range(table.columns):
                cell = TableCell.objects.filter(table=table, row=row_number, column=column_number).first()
                row.append(cell)
            rows.append({'cells': row})
    return render(request, 'folder_view.html',
                  {'folder': folder, 'table': {'rows': rows} if table else None, 'table_id': table_id})


def table_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    table = Table.objects.filter(folder=folder).first()
    rows = []
    table_id = None
    if table:
        table_id = table.id
        for row_number in range(table.rows):
            row = []
            for column_number in range(table.columns):
                cell = TableCell.objects.filter(table=table, row=row_number, column=column_number).first()
                row.append(cell)
            rows.append({'cells': row})
    return render(request, 'table_view.html',
                  {'folder': folder, 'table': {'rows': rows} if table else None, 'table_id': table_id})


def get_max_folder_index(request):
    max_index = Folder.objects.aggregate(Max('index'))['index__max'] or 0
    return JsonResponse({'max_index': max_index})


@csrf_exempt
def save_table(request):
    if request.method == "POST":
        data = json.loads(request.body)
        folder_id = data['folder_id']
        rows = int(data['rows'])
        columns = int(data['columns'])
        folder = Folder.objects.get(id=folder_id)
        table = Table.objects.filter(folder=folder).first()
        if table:
            table.rows = rows
            table.columns = columns
            table.save()
            table.cells.all().delete()
        else:
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
def delete_table_in_folder(request, folder_id):
    if request.method == "POST":
        folder = get_object_or_404(Folder, id=folder_id)
        table = Table.objects.filter(folder=folder).first()
        if table:
            table.delete()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'No table found in folder'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def explorer_view(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    if not folder.is_local_link:
        return JsonResponse({'status': 'error', 'message': 'Not a local link'})

    folder_path = folder.link.replace('file://', '')
    try:
        contents = get_folder_contents_data(folder_path)
        return render(request, 'explorer.html', {
            'folder': folder,
            'contents': contents,
            'current_path': folder_path
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def get_folder_contents(request):
    folder_id = request.GET.get('folder_id')
    try:
        folder_id = int(folder_id)
        folder = get_object_or_404(Folder, id=folder_id)
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid folder ID'})

    if folder.is_local_link:
        folder_path = folder.link.replace('file://', '')
        try:
            contents = get_folder_contents_data(folder_path)
            return JsonResponse({
                'status': 'success',
                'contents': contents,
                'current_path': folder_path
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Not a local folder'})


def get_folder_contents_data(folder_path):
    with os.scandir(folder_path) as entries:
        return [{
            'id': str(entry.path),  # Преобразуем путь в строку
            'name': entry.name,
            'is_dir': entry.is_dir(),
            'size': entry.stat().st_size if not entry.is_dir() else 0,
            'last_modified': datetime.fromtimestamp(entry.stat().st_mtime).isoformat(),
            'file_type': 'folder' if entry.is_dir() else mimetypes.guess_type(entry.path)[0],
            'icon': get_icon_path('folder' if entry.is_dir() else mimetypes.guess_type(entry.path)[0])
        } for entry in entries]


def get_icon_path(file_type):
    icon_mapping = {
        'folder': 'shortcuts/folder.png',
        'text': 'shortcuts/txt-file.png',
        'image': 'shortcuts/image.png',
        'audio': 'shortcuts/audio.png',
        'video': 'shortcuts/video.png',
        'pdf': 'shortcuts/pdf.png',
        'word': 'shortcuts/word.png',
        'excel': 'shortcuts/excel.png',
        'archive': 'shortcuts/archive.png',
        'unknown': 'shortcuts/unknown.png'
    }

    base_type = file_type.split('/')[0] if file_type else 'unknown'

    if file_type in ['application/pdf']:
        return f'/static/{icon_mapping["pdf"]}'
    elif file_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        return f'/static/{icon_mapping["word"]}'
    elif file_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
        return f'/static/{icon_mapping["excel"]}'
    elif file_type in ['application/zip', 'application/x-rar-compressed', 'application/x-7z-compressed']:
        return f'/static/{icon_mapping["archive"]}'
    elif base_type in icon_mapping:
        return f'/static/{icon_mapping[base_type]}'
    else:
        return f'/static/{icon_mapping["unknown"]}'


def file_action(request):
    action = request.GET.get('action')
    path = request.GET.get('path')

    if not os.path.exists(path):
        return JsonResponse({'status': 'error', 'message': 'File not found'})

    if action == 'open':
        file_type, encoding = mimetypes.guess_type(path)
        if file_type:
            with open(path, 'rb') as file:
                response = FileResponse(file)
                response['Content-Type'] = file_type
                response['Content-Disposition'] = f'inline; filename="{os.path.basename(path)}"'
                return response
        else:
            return JsonResponse({'status': 'error', 'message': 'Unable to determine file type'})

    elif action == 'download':
        with open(path, 'rb') as file:
            response = FileResponse(file)
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
            return response

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid action'})