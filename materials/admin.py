from django.contrib import admin
from .models import Material


# Register your models here.

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'type', 'quantity', 'latitude', 'longitude', 'contact_name', 'contact_phone', 'is_active'
    )
    list_filter = ('is_active', 'type')
    search_fields = ('name', 'location')


