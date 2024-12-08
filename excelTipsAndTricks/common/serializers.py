# serializers.py
from rest_framework import serializers
from .models import AboutPage

class AboutPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPage
        fields = ['title', 'description']
