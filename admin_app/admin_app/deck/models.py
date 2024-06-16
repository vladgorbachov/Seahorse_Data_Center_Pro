# admin_app/admin_app/deck/models.py
from django.db import models

class Folder(models.Model):
    index = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)
    visible = models.BooleanField(default=True)  # Поле для отслеживания видимости папки

    def __str__(self):
        return self.name

class Table(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='tables')
    rows = models.IntegerField()
    columns = models.IntegerField()

class TableCell(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='cells')
    row = models.IntegerField()
    column = models.IntegerField()
    content = models.TextField(blank=True)
