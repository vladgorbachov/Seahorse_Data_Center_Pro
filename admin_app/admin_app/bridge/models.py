from django.db import models


class Folder(models.Model):
    objects = None
    index = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=2048, blank=True, null=True)
    is_local_link = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='subfolders')
    is_file = models.BooleanField(default=False)
    department = models.CharField(max_length=10, choices=[('deck', 'Deck'), ('bridge', 'Bridge')], default='deck')

    def __str__(self):
        return self.name


class FileMetadata(models.Model):
    folder = models.OneToOneField(Folder, on_delete=models.CASCADE, related_name='metadata')
    file_type = models.CharField(max_length=50, blank=True, null=True)
    size = models.BigIntegerField(default=0)
    last_modified = models.DateTimeField(null=True, blank=True)
    icon_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Metadata for {self.folder.name}"


class Table(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='tables')
    rows = models.IntegerField()
    columns = models.IntegerField()


class TableCell(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='cells')
    row = models.IntegerField()
    column = models.IntegerField()
    content = models.TextField(blank=True)


class DPHours(models.Model):
    date = models.DateField(unique=True)
    hours = models.IntegerField()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.date}: {self.hours} hours"
