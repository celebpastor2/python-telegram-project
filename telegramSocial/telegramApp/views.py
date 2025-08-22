from django.shortcuts import render
from django.http import HttpResponse
from .models import TelegramUsers
from .models import Friends
from .models import Products
import json


class RegisterUser():
    people = []
    def get(request):
        render("index")

    def post(request):
        details = request.POST

        try :
            TelegramUsers.objects.create(chat_id=details['chat_id'], first_name=details['first_name'])
            gramUsers = TelegramUsers()
            gramUsers.chat_id = details['chat_id']
            gramUsers.first_name = details['first_name']
            gramUsers.save()
        except :
            return HttpResponse("Error Registering User")
    
    def put(request):
        return HttpResponse("You've made a put request on this server")

# Create your views here.
def name(request):
    return HttpResponse( "something" )

def userExist(request):
    id = request.GET.get("id")
    chat_id = request.GET.get("chat_id")
    isExist = TelegramUsers.objects.filter(chat_id=chat_id)

    if isExist :
        return HttpResponse(json.dumps(isExist)) 

    
    return HttpResponse("User not Exist")

def registerUser(request):
    details = request.POST

    try :
        TelegramUsers.objects.create(chat_id=details['chat_id'], first_name=details['first_name'], last_name=details['last_name'], socials="{}")
        HttpResponse("User Successfully Created")
    except :
        return HttpResponse("Error Registering User")
    
def getTelegramUser(request):
    chat_id = request.GET.get("chat_id")
    users = TelegramUsers.objects.filter(chat_id=chat_id)
    HttpResponse(json.dumps(users))

def addTelegramUserFriend(request):
    friend_id = request.POST.get("friend_id")
    chat_id = request.POST.get("chat_id")
    user = TelegramUsers.objects.filter(chat_id=chat_id)
    friend = TelegramUsers.objects.filter(chat_id=friend_id)

    if friend :
        user_id = user.__id
        Friends.objects.create(friend_id=friend_id, chat_id=chat_id, user_id=user_id,user=user)
        return HttpResponse("User Successfully Created")
    

    else : 
        return HttpResponse("Friend Indicated Not Found")


def removeTelegramUserFriend(request):
    friend_id = request.POST.get("friend_id")
    chat_id = request.POST.get("chat_id")
    friend = Friends.objects.filter(chat_id=chat_id, friend_id=friend_id)

    if friend :
        friend.delete()
        return HttpResponse("Friend Successfully Deleted")

    else :
        return HttpResponse("Friend not found")
    

def getAllTelegramFriend(request):
    chat_id = request.POST.get("chat_id")
    user    = TelegramUsers.objects.filter(chat_id=chat_id)
    friends = user.select_related("friends")

    if friends :
        return HttpResponse(json.dumps(friends))
    
    else :
        return HttpResponse("{}")
    
def getAllTelegramGroups(request):
    chat_id = request.POST.get("chat_id")
    user    = TelegramUsers.objects.filter(chat_id=chat_id)
    groups = user.select_related("groups")

    if groups :
        return HttpResponse(json.dumps(groups))
    
    else :
        return HttpResponse("{}")
    
def getAllTelegramPost(request):
    chat_id = request.POST.get("chat_id")
    user    = TelegramUsers.objects.filter(chat_id=chat_id)
    posts = user.select_related("posts")

    if posts :
        return HttpResponse(json.dumps(posts))
    
    else :
        return HttpResponse("{}")
    
def get_products(request):
    products = Products.objects.filter(available=True)
    return render(request, 'products/product_list.html', {'products': products})







#model view template kind of framework
