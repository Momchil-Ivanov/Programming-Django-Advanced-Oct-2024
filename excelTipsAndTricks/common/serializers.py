from rest_framework import serializers


class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100)
    temperature = serializers.FloatField()
    description = serializers.CharField(max_length=255)
    icon = serializers.CharField(max_length=100)
