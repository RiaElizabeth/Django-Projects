from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300, default=None)
    date = models.DateTimeField(default=datetime.datetime.now)
    liked = models.ManyToManyField(User, blank = True, related_name="postlikes")

    
class Follower(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user',default=None)
    follower = models.ManyToManyField(User, related_name='follower', default=None)
    following = models.ManyToManyField(User, related_name='following', default=None)
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
