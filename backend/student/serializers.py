from .models import *
from rest_framework import serializers
from faculty.serializers import FacultySerializer
from year.serializers import YearSerializer
from section.serializers import SectionSerializer

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields =  ['faculty','dob','gender','contactNumber','year','address','joinDate','collegeMail','section','email','full_name','password','user_type','image']


class FetchStudentSerializer(serializers.ModelSerializer):
    year = YearSerializer()
    faculty = FacultySerializer()
    section = SectionSerializer()
    class Meta:
        model = Student
        fields =  ['id','faculty','dob','gender','contactNumber','year','address','joinDate','collegeMail','section','email','full_name','user_type','image']
