from rest_framework import serializers
from .models import Stork
# from .models import Bitcoin

class StorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stork
        fields = ['stork_id', 'name']

# class BitCoinSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bitcoin
#         fields = ['market', 'name', 'eng_name']