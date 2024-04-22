from django.db import models
from year.models import *
from faculty.models import *
from teacher.models  import Teacher
# Create your models here.
class Module(models.Model): 
    module_name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.module_name + f" {self.id}"

class ModuleYear(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    module_start_date = models.DateField()
    module_end_date = models.DateField()
    module = models.ForeignKey(Module,on_delete=models.CASCADE)

class ModuleTeacher(models.Model):
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)