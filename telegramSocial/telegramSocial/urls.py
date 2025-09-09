"""
URL configuration for telegramSocial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from telegramApp.views import name
from telegramApp.views import RegisterUser
from telegramApp.views import userExist
from telegramApp.views import getAllTelegramGroups
from telegramApp.views import getAllTelegramFriend
from telegramApp.views import getAllTelegramUser
from telegramApp.views import removeTelegramUserFriend
from telegramApp.views import addTelegramUserFriend
from telegramApp.views import getTelegramUser
from telegramApp.views import get_products
from telegramApp.views import create_product
from telegramApp.views import update_product
from telegramApp.views import index
from telegramApp.views import createTelegramGroup
from telegramApp.views import updateTelegramGroup
from telegramApp.views import createPost
from telegramApp.views import topup
from telegramApp.views import product_create_page
from telegramApp.views import share_post
from telegramApp.views import create_post_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('view/', name),
    path('class/', RegisterUser),
    path("exists/", userExist),
    path("get-telegram-group/", getAllTelegramGroups),
    path("create-user-group/", createTelegramGroup),
    path("update-user-group/", updateTelegramGroup),
    path("get-telegram-friends/", getAllTelegramFriend),
    path("remove-telegram-friends/", removeTelegramUserFriend),
    path("add-telegram-friend/", addTelegramUserFriend),
    path("get-telegram-user/", getTelegramUser),
    path("get-telegram-users/", getAllTelegramUser),
    path('get-products/', get_products, name='get_products'),
    path('create-post/', createPost),
    path('create-product/', create_product, name='create_product'),
    path('update-product/', update_product, name='update_product'),
     path('topup/', topup),
    path("", index),
    path("create-page/", product_create_page),
    path("post-page/", create_post_page),
    path("share-post/", share_post),
    path("submit-product/", create_product)
]
