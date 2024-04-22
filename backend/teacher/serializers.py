from .models import *
from rest_framework import serializers
from faculty.serializers import FacultySerializer
from year.serializers import YearSerializer
from section.serializers import SectionSerializer


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields =  ['faculty','dob','gender','contactNumber','address','joinDate','collegeMail','email','full_name','password','user_type','image','qualification','experience']

class FetchTeacherSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()
    class Meta:
        model = Teacher
        fields = ['id','faculty','dob','gender','contactNumber','address','joinDate','collegeMail','email','full_name','user_type','image','qualification','experience']