from django.db import models
from users.models import *
from django.utils import timezone

# Create your models here.
class Admin(BaseUser):
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.date