from django.shortcuts import render
from django.http import HttpResponse
from .models import TelegramUsers
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
        TelegramUsers.objects.create(chat_id=details['chat_id'], first_name=details['first_name'])
    except :
        return HttpResponse("Error Registering User")
    
def getTelegramUser(request):
    chat_id = request.GET.get("chat_id")
    users = TelegramUsers.objects.filter(chat_id=chat_id)
    HttpResponse(json.dumps(users))





#model view template kind of framework
