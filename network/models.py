from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    body = models.TextField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "date": self.date
        }

    def __str__(self) -> str:
        return f"By {self.author} on {self.date}"
    
    def is_valid(self):
        if self.body.split():
            return True
        return False


class Like(models.Model):
    liker = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    