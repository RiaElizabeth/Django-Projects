from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting = models.FloatField()
    image = models.TextField()
    created_date = models.DateTimeField(default=timezone.now, editable = False)
    category = models.CharField(max_length=80)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Title: {self.title}"+"\n"+f"Description: {self.description}"+"\n"+f"Starting bid: {self.starting}"+"\n"+f"Image URL: {self.image}"+"\n"+f"Category: {self.category}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding_user")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bid_item")
    new_bid = models.FloatField()
    count = models.IntegerField(default=1)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    item = models.ForeignKey(Auction, on_delete=models.CASCADE, default=None, related_name="comment_item")
    date_pub = models.DateTimeField(default=timezone.now, editable =False)
    new_comment = models.TextField()

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_user")
    item = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="watch_item")
