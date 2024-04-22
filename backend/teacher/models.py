from django.db import models
from faculty.models import *
from users.models import *

class Teacher(BaseUser):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    contactNumber = models.CharField(max_length=20)
    address = models.TextField()
    joinDate = models.DateField()
    collegeMail = models.EmailField()
    qualification = models.CharField(null=True,max_length=50)
    experience = models.CharField(null=True,max_length=50)
    def __str__(self):
        return self.full_name + f" {self.id}"