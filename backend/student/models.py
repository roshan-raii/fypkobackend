from django.db import models
from year.models import *
from faculty.models import *
from section.models import *
from users.models import *


class Student(BaseUser):
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    contactNumber = models.CharField(max_length=20)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    address = models.TextField()
    joinDate = models.DateField()
    collegeMail = models.EmailField()

    def __str__(self):
        return self.full_name
    