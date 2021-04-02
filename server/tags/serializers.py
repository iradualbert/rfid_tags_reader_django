from django.db.models import fields
from rest_framework import serializers
from .models import Tag, Entry


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        
        