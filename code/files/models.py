from django.db import models
import os

# Create your models here.

class UploadedFile(models.Model):
    file_itself = models.FileField()
    name = models.CharField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True, default=None, null=True)
    upload_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file_itself.name
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file_itself.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
