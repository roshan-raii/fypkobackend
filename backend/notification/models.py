from django.db import models

class Notification(models.Model):
    notificationID = models.AutoField(primary_key=True)
    content = models.TextField()

    def __str__(self):
        return f"Notification {self.notificationID}"