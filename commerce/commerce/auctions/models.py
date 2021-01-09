from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    startingbid = models.DecimalField(max_digits=64, decimal_places=2)
    description = models.TextField()
    image = models.URLField()
    creator = models.CharField(max_length=64)

class Bid(models.Model):
    user = models.CharField(max_length=64)
    bid = models.DecimalField(max_digits=64, decimal_places=2)
    listingid = models.IntegerField()

class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.CharField(max_length=64)
    listingid = models.IntegerField()

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()

class Closedbid(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listingid = models.IntegerField()
    winprice = models.IntegerField()
