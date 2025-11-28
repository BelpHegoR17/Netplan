from django.db import models

# Create your models here.

class Device(models.Model):
    DEVICE_TYPES = [
        ('ROUTER','Router'),
        ('SWITCH','Switch'),
        ('AP','Access Point'),
    ]

    STATUS_CHOICES = [
        ('UP','Online'),
        ('DOWN','Offline'),
        ('MAINT','Maintenance'),
    ]

    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=17, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DOWN')
    added_on = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=30)

    def _str_(self):
        return f"{self.name} ({self.ip_address})"