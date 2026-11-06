from django.db import models
from django.conf import settings


class Activity(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('declined', 'Declined'),
    ]

    activity_id = models.CharField(max_length=100, unique=True)

    stationary_profile = models.ForeignKey(
        'StationaryProfile',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='activities'
    )

    activity_type = models.CharField(max_length=100)

    costs = models.DecimalField(max_digits=10, decimal_places=2)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    sent_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default='waiting'
    )

    def __str__(self):
        return f"{self.activity_id} - {self.activity_type}"
    



class DocumentFormat(models.Model):
    activity = models.OneToOneField(
        Activity,
        on_delete=models.CASCADE,
        related_name='document_format'
    )

    font_family = models.CharField(max_length=100)
    font_size = models.CharField(max_length=100)
    text_alignment = models.CharField(max_length=100)
    other_details = models.CharField(max_length=240)

    def __str__(self):
        return f"Format for {self.activity.activity_id}"