from rest_framework import serializers
from .models import *

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = "__all__"