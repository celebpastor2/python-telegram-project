from django.contrib import admin
from .models import Posts
from .models import Friends
from .models import Groups
from .models import TelegramUsers

# Register your models here.
admin.site.register(Posts)
admin.site.register(Friends)
admin.site.register(Groups)
admin.site.register(TelegramUsers)
