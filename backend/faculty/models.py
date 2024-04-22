from django.db import models

# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length = 50,unique = True)

    def __str__(self):
        return self.name + f" {self.id}"