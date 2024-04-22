from django.db import models
from year.models import Year
from faculty.models import Faculty
# from section.models import Section÷
# Create your models here.
class Section(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name

class YearSection(models.Model):
    year = models.ForeignKey(Year,on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    def __str__(self):
        return (f"THe year {self.year.name} The section: {self.section.name}")