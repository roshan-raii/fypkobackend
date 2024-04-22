from rest_framework import serializers
from .models import *
from year.serializers import *
from faculty.serializers import FacultySerializer

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"

class YearSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearSection
        fields = "__all__"


class FetchYearSecationSerializer(serializers.ModelSerializer):
    year = YearSerializer()
    section = SectionSerializer()
    faculty = FacultySerializer()
    class Meta:
        model = YearSection
        fields = "__all__"