from django.db import models

class Folder(models.Model):
    index = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)
    visible = models.BooleanField(default=True)  # Поле для отслеживания видимости папки

    def __str__(self):
        return self.name
