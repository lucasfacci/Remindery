from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.AutoField(primary_key=True)

class Agenda(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    color = models.CharField(max_length=25, null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class Reminder(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255, null=False)
    date = models.DateField(null=False)
    scratched = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)