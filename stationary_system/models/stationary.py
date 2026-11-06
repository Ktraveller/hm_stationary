from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class StationaryProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    stationary_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(default='', blank=True)
    force_password_change = models.BooleanField(default=True)

    # Merchant number
    payment_no = models.CharField(max_length=10, unique=True, blank=False, null=False)
    payment_name = models.CharField(max_length=100, blank=False, null=False)

    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



# stationary location
class Area(models.Model):
    stationary = models.ForeignKey(
        'StationaryProfile',
        on_delete=models.CASCADE,  # ← automatically deletes Area if StationaryProfile is deleted
        related_name='areas'
    )
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.stationary.stationary_name} Location"

