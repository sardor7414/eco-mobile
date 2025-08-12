from rest_framework import serializers
from .models import Material


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class MaterialContactSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source='user.first_name')  # yoki .name agar shunday bo‘lsa
    contact_phone = serializers.CharField(source='user.phone')
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    type = serializers.CharField()

    class Meta:
        model = Material
        fields = ['type', 'contact_name', 'contact_phone', 'quantity']


class MaterialMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'type', 'quantity', 'latitude', 'longitude']