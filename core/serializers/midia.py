from rest_framework import serializers
from core.models.midia import Midia

class MidiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Midia
        fields = '__all__'