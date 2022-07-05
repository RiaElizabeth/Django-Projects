from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Team(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ManyToManyField(User, related_name='owner')
    user = models.ManyToManyField(User, related_name='user')

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "owner": [ownervalue.username for ownervalue in self.owner.all()],
            "user": [uservalue.username for uservalue in self.user.all()]
        }

class Task(models.Model):
    title = models.CharField(max_length=200, null=True)
    assignee = models.ManyToManyField(User, related_name='assignee')
    assigned = models.ManyToManyField(User, related_name='assigned')
    due = models.DateField(null=True)
    description = models.CharField(max_length=500, null=True)
    completed = models.BooleanField(default=False)

class Workflow(models.Model):
    title = models.CharField(max_length=200, null=True)
    team = models.ManyToManyField(Team, related_name='team')
    task = models.ManyToManyField(Task, related_name='task')