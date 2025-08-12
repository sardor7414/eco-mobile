from django.conf import settings
from django.db import models



# Create your models here.

class DefaultAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Material(DefaultAbstract):
    MATERIAL_TYPES = [
        ('metal', 'Metal'),
        ('paper', 'Paper'),
        ('plastic', 'Plastic'),
        ('glass', 'Glass'),
        ('organic', 'Organic'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  # kg yoki tonna
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)  # Yangi maydon

    def __str__(self):
        return f"{self.type} - {self.quantity}kg"
