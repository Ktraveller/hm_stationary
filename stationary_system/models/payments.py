from django.db import models
from django.conf import settings


class Payments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stationary_profile = models.ForeignKey(
        'StationaryProfile',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='payments'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    phone_used = models.CharField(max_length=10, null=False, blank=False)
    description = models.TextField(blank=True, null=True)

    paid_at = models.DateTimeField(blank=True, null=True)