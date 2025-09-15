from .models import TelegramUsers
from .models import Products
from django import forms


class UserForm( forms.ModelForm ):
    class Meta:
        model = TelegramUsers
        fields = ["first_name", "last_name", "phone_number", "username", "chat_id", "location"]


class ProductForm( forms.ModelForm ):
    class Meta:
        model = Products
        fields = ["name", "image", "description", "price", "stock"]