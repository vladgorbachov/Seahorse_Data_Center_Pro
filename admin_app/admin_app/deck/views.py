from django.db.models import Max
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Folder
from django.views.decorators.csrf import csrf_exempt
import json

def deck_department(request):
    folders = Folder.objects.filter(visible=True)  # Загружаем только видимые папки
    return render(request, 'deck_department.html', {'folders': folders})

@csrf_exempt
def add_folder(request):
    if request.method == "POST":
        data = json.loads(request.body)
        folder = Folder(index=data['index'], name=data['name'], link=data.get('link', ''), visible=True)
        folder.save()
        return JsonResponse({'status': 'success', 'id': folder.id})

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
    folder = Folder.objects.get(id=folder_id)
    return render(request, 'folder_view.html', {'folder': folder})

def get_max_folder_index(request):
    max_index = Folder.objects.aggregate(Max('index'))['index__max'] or 0
    return JsonResponse({'max_index': max_index})
