from rest_framework import serializers
from .models import *
from teacher.serializers import *
class ModuleSerialier(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"

class ModuleYearSerialier(serializers.ModelSerializer):
    module = ModuleSerialier()
    class Meta:
        model = ModuleYear
        fields = "__all__"

class ModuleYearSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleYear
        fields = "__all__"


class FetchModuleTeacherSerializer(serializers.ModelSerializer):
    module = ModuleSerialier()
    teacher = FetchTeacherSerializer()
    class Meta:
        model = ModuleTeacher
        fields = "__all__"
class ModuleTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleTeacher
        fields = "__all__"