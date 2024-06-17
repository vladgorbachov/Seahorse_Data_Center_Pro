from django.db import models


class Folder(models.Model):
    index = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=2048, blank=True, null=True)
    is_local_link = models.BooleanField(default=False)
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
