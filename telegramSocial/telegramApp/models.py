from django.db import models

class TelegramUsers(models.Model):
    first_name  = models.CharField(max_length=255, null=True)
    last_name   = models.CharField(max_length=255, null=True)
    phone_number   = models.CharField(max_length=30, default="", null=True)
    username   = models.CharField(max_length=255, default="", null=True)
    location   = models.CharField(default="", null=True)
    chat_id     = models.CharField(max_length=255, unique=True)   
    balance     = models.FloatField( default=0.00) 
    referee     = models.BigIntegerField(default= 0)  
    socials   = models.JSONField(null=True)

class Groups(models.Model):
    group_id = models.CharField(max_length=40, unique=True)
    members = models.TextField(default="[]")
    group_name=models.CharField(max_length=100)
    group_description=models.TextField()
    group_settings = models.TextField(default="[]")
    telegram      = models.ForeignKey(TelegramUsers, on_delete=models.RESTRICT, to_field="chat_id", default=None)

class Posts(models.Model):
    post_id = models.CharField(max_length=30, unique=True)
    content = models.TextField()
    target  = models.CharField(max_length=10)    
    telegram       = models.ForeignKey(TelegramUsers, on_delete=models.RESTRICT, to_field="chat_id", default=None)

class Sharedpost(models.Model):
    post_id = models.CharField(max_length=30, unique=True) 
    original_post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='shares')
    shared_at = models.DateTimeField(auto_now_add=True)
    shared_by = models.DateTimeField(auto_now_add=True)




class Friends(models.Model):
    friend_id = models.CharField(unique=True, max_length=100)
    chat_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    telegram =  models.ForeignKey(TelegramUsers, on_delete=models.RESTRICT, to_field="chat_id", default=None)

class Products(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    user    = models.ForeignKey(TelegramUsers, on_delete=models.RESTRICT, to_field="chat_id")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Topup(models.Model):
    chat_id = models.CharField(max_length=255)
    payload = models.JSONField(unique=True)
    name = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True)
    email = models.JSONField(null=True)
    phone_number   = models.CharField(max_length=30, default="", null=True)
    shipping_address = models.CharField(max_length=255, null=True)
    currency = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    