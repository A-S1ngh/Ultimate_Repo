from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    body = models.CharField(max_length = 180)
    timestamp = models.DateTimeField()
    likecount = models.IntegerField(default=0)

    def serialize(self):
        return {
            "likecount":self.likecount
        }

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likeduser")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likedpost")
