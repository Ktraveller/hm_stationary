from django.db import models


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    processed_file = models.FileField(upload_to='uploads/', null=True, blank=True)

    activity = models.ForeignKey(
        'Activity',
        on_delete=models.CASCADE,
        related_name='uploaded_files'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity.activity_id} - {self.file.name}"