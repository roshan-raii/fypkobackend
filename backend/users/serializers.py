from .models import *
from rest_framework import serializers

class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ["email", "password"]