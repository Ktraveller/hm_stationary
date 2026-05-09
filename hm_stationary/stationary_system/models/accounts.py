from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    stationary_id = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username
    

# notification
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.message[:20]}"