from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    postContent = models.TextField(blank=False)
    dateTime = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveSmallIntegerField(default=0, blank=True, null=True)

    def serialize(self):
        return {
            "id": self.id,
            "postContent": self.postContent,
            "dateTime": self.dateTime.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": self.likes
        }

class UserFollowers(models.Model):
    specificUser = models.ForeignKey("User", on_delete=models.CASCADE, related_name="UserOfFollowers")
    followers = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followersOfUser")

class UserFollowing(models.Model):
    specificUser = models.ForeignKey("User", on_delete=models.CASCADE, related_name="UserWhoFollows")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="FollowsOfUser")

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="userWhoLikes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likedPost")
