# notifications/models.py

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)  # Optional FCM token

    def __str__(self):
        return self.name
