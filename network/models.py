from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    date = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return f"Post {self.id} by {self.user} at {self.date.strftime('%H:%M:%S %d %b %Y')} and liked {self.liked.count()}"
    
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")

    def __str__(self):
        return f"{self.user} is following {self.user_follower}"
    
