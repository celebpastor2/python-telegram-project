from django.db import models

class TelegramUsers(models.Model):
    first_name  = models.CharField(max_length=255)
    last_name   = models.CharField(max_length=255)
    chat_id     = models.CharField(max_length=255, unique=True)   
    socials   = models.JSONField()

class Groups(models.Model):
    group_id = models.CharField(max_length=40, unique=True)
    members = models.TextField()
    group_name=models.CharField(max_length=100)
    group_description=models.TextField()
    group_settings = models.TextField()
    telegram      = models.ForeignKey(TelegramUsers, on_delete=models.RESTRICT, to_field="chat_id", default=None)

class Posts(models.Model):
    post_id = models.CharField(max_length=30, unique=True)
    content = models.TextField()
    target  = models.CharField(max_length=10)    
    telegram       = models.ForeignKey(TelegramUsers, on_delete=models.RESTRICT, to_field="chat_id", default=None)


# Create your models here.


class Friends(models.Model):
    friend_id = models.CharField(unique=True, max_length=100)
    chat_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    telegram =  models.ForeignKey(TelegramUsers, on_delete=models.RESTRICT, to_field="chat_id", default=None)

class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)