from django.db import models

class Friends(models.Model):
    friend_id = models.CharField(unique=True, max_length=100)
    chat_id = models.BigIntegerField()
    user_id = models.BigIntegerField()

class Groups(models.Model):
    group_id = models.CharField(max_length=40, unique=True)
    members = models.TextField()
    group_name=models.CharField(max_length=100)
    group_description=models.TextField()
    group_settings = models.TextField()

class Posts(models.Model):
    post_id = models.CharField(max_length=30, unique=True)
    content = models.TextField()
    target  = models.CharField(max_length=10)


# Create your models here.
class TelegramUsers(models.Model):
    first_name  = models.CharField(max_length=255)
    last_name   = models.CharField(max_length=255)
    chat_id     = models.CharField(max_length=255)
    friends     = models.ForeignKey(Friends, on_delete=models.RESTRICT, to_field="friend_id")
    groups      = models.ForeignKey(Groups, on_delete=models.RESTRICT, to_field="group_id")
    posts       = models.ForeignKey(Posts, on_delete=models.RESTRICT, to_field="post_id")
    socials   = models.JSONField()