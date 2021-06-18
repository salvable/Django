from rest_framework import serializers
from .models import Bitcoin

class BitCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bitcoin
        fields = ['market', 'name', 'eng_name']