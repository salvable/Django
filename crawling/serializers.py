from rest_framework import serializers
from .models import Stork


class StorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stork
        fields = ['no', 'name']