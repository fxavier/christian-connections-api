from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    email = models.EmailField(
        blank=False, max_length=254, verbose_name="email address")

    USERNAME_FIELD = 'username'   # e.g: "username", "email"
    EMAIL_FIELD = 'email'


class Like(models.Model):
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title


class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=150)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
