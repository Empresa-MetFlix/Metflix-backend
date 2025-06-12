from rest_framework import serializers
from core.models import Category, Media, Rental

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = "__all__"