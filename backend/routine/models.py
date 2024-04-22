from django.db import models
from year.models import *
from section.models import *
from module.models import *


class Routine(models.Model):
    day = models.CharField(max_length=20)
    time = models.TimeField()
    module = models.ForeignKey(Module,on_delete=models.CASCADE,null=True)
    year_section = models.ForeignKey(YearSection,on_delete=models.CASCADE)

    def __str__(self):
        return f"Routine {self.id}"
