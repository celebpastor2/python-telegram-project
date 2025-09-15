from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import TelegramUsers
from .models import Friends
from .models import Products
from .models import Posts
from .models import Groups
from .models import Topup
from django.db.utils import IntegrityError
from .forms import UserForm
from .forms import ProductForm

import json


class RegisterUser():
    people = []
    def get(request):
        render("index")

    

def product_create_page(request):
    form = ProductForm()
    return render(request, "product_create.html", {
        "form"  : form
    })

def create_post_page(request):

    return render(request, "create_post.html")



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
    users = TelegramUsers.objects.filter(chat_id=chat_id).first()

    if users :
        return JsonResponse(model_to_dict(users))
    
    return HttpResponse("No User Found")

def getAllTelegramUser(request):
    users = TelegramUsers.objects.all()
    users = [model_to_dict(u) for u in users]
    return JsonResponse(users,safe=False)

@csrf_exempt
def addTelegramUserFriend(request):
    friend_id = request.POST.get("friend_id")
    chat_id = request.POST.get("chat_id")

    try :
        user = TelegramUsers.objects.filter(chat_id=chat_id).first()
        friend = TelegramUsers.objects.filter(chat_id=friend_id).first()

        if friend :
            user_id = user.chat_id
            Friends.objects.create(friend_id=friend_id, chat_id=chat_id, user_id=user_id,telegram=user)
            return HttpResponse("Friend Successfully Established")
        

        else : 
            return HttpResponse("Friend Indicated Not Found")
        
    except IntegrityError as e:        
        return HttpResponse(f"Friend with ID: {friend_id} Already Accepted")
    
    except Exception as e :
        print(e)
        return HttpResponse("Friend Indicated does not Exists")


def removeTelegramUserFriend(request):
    friend_id = request.POST.get("friend_id")
    chat_id = request.POST.get("chat_id")
    friend = Friends.objects.filter(chat_id=chat_id, friend_id=friend_id)

    if friend :
        friend.delete()
        return HttpResponse("Friend Successfully Deleted")

    else :
        return HttpResponse("Friend not found")
    
@csrf_exempt
def getAllTelegramFriend(request):
    chat_id = request.POST.get("chat_id")
    user    = TelegramUsers.objects.filter(chat_id=chat_id).first()

    if not user :
        return HttpResponse("['user not found']")

    friends = Friends.objects.filter(chat_id=user.chat_id )

    if friends :
        try :        
            return HttpResponse(json.dumps( [model_to_dict(TelegramUsers.objects.filter(chat_id=f.friend_id).first()) for f in friends ] ))
        
        except Exception as e :
            print(e)

    
    else :
        return HttpResponse("[]")
    
def getAllTelegramGroups(request):
    chat_id = request.POST.get("chat_id")
    user    = TelegramUsers.objects.filter(chat_id=chat_id)
    groups = user.select_related("groups")

    if groups :
        return HttpResponse(serializers.serialize("json", groups))
    
    else :
        return HttpResponse("{}")
    
def createTelegramGroup(request):
    chat_id = request.POST.get("chat_id")
    group_id = request.POST.get("group_id")
    user    = TelegramUsers.objects.filter(chat_id=chat_id)

    if user :
       Groups.objects.create(group_id=group_id, telegram=user)
    
    else :
        return HttpResponse("Group Creator Does not Exists")
    
def updateTelegramGroup(request):
    chat_id = request.POST.get("chat_id")
    setting = request.POST.get("setting")
    group_id = request.POST.get("group_id")
    description = request.POST.get("description")
    name = request.POST.get("group_name")
    group    = Groups.objects.filter(group_id=group_id).first()

    if group :
        if name : 
            group.group_name = name
        
        if description :
            group.group_description = description

        if chat_id :
            members = group.members

            members = json.loads(members)
            
            members.append(chat_id)
            members = json.dumps(members)
            group.members = members

        if setting : 
            settings = json.loads( group.group_settings )
            settings.append(setting)
            group.group_settings = json.dumps(settings)
       
        group.save()
        return HttpResponse("Group Successfully Updated")
    
    else :
        return HttpResponse("Group Does not Exists")
    
def getAllTelegramPost(request):
    chat_id = request.POST.get("chat_id")
    user    = TelegramUsers.objects.filter(chat_id=chat_id)
    posts = user.select_related("posts")

    if posts :
        return HttpResponse(serializers.serialize("json",posts))
    
    else :
        return HttpResponse("{}")
    
def load_balance(request):
    chat_id     = request.POST.get("chat_id")
    amount  = request.POST.get("amount")
    payload = request.POST.get("payload")
    user    = TelegramUsers.objects.filter(chat_id=chat_id).first()
    topup   = Topup.objects.filter(chat_id=chat_id).first()

    if user :        
        balance     = float( user.balance )
        new_balance = balance + float(amount)
        
        if topup and topup.payload == payload:
            user.balance    = new_balance
            user.save()
            JsonResponse(data={
                "success"   : True,
                "balance"   : new_balance,
                "old_balance"   : balance,
                "chat_id"   : chat_id
            })
            topup.delete()
        else :
            JsonResponse(data={
                "success"   : False,
                "message"   : "Couldn't find a corresponding topup data"
            })

    else :
        JsonResponse(data={
            "success"   : False,
            "message": "User not found"
        })


    
def get_products(request):
    products = list( Products.objects.select_related("user").filter(available=True))
    page    = int( request.GET.get("page") or 0 )

    if not page :
        products = products[:15]

    else :
        start = 15 * page
        end    = start + 15
        products = products[start:end]

    return HttpResponse(serializers.serialize("json", products))

def create_product(request):

    try :
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.POST.get("image")#this works with telegram bot
        stock = int( request.POST.get("stock") )
        user_id = int( request.POST.get("user") )

        if not image: 
            image = request.FILES.get("image")

        user = TelegramUsers.objects.get(chat_id=user_id)

        print(model_to_dict(user))

        if user :
            Products.objects.create(name=name, price=price, description=description, stock=stock, image=image, user=user)
            return HttpResponse("Product Successfully Created")

        else : 
            #link the product t a default 
            return HttpResponse("No User in Request or User not Register with this bot")     

    except Exception as e:
        print(e)
        return HttpResponse("Error Creating product to database")
    
def update_product(request):

    try :
        id = request.POST.get("id")
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        stock = int( request.POST.get("stock") )
        user_id = int( request.POST.get("user") )

        product = Products.objects.get(_id = id)

        if product :
            if price :
                product.price = price
            
            if name :
                product.name = name

            if description :
                product.description = description
            
            if stock :
                product.stock = stock

            product.save(True)
            return HttpResponse("Product Successfully Updated")
        
        elif name and price and description and stock and user_id :
            user = TelegramUsers.objects.filter(chat_id=user_id)

            if user :
                Products.objects.create(name=name, price=price, description=description, stock=stock, user=user)
                return HttpResponse("Product Successfully Created")

            else : 
                #link the product t a default 
                return HttpResponse("No User in Request or User not Register with this bot")
        else :
            return HttpResponse("Product Not Found!")     

    except :
        return HttpResponse("Error Creating product to database")
    #image = request.FILES.get("image")



def index(request):
    chat_id = request.GET.get("chat_id")
    first_name = request.GET.get("first_name")
    last_name = request.GET.get("last_name")
    phone_number = request.GET.get("phone_number")
    username = request.GET.get("username")
    location = request.GET.get("location")

    try :

        user = TelegramUsers.objects.filter(chat_id=chat_id).first()

        if user :
            user.first_name = first_name
            user.last_name = last_name 
            user.username = username 
            user.location = location or ""
            user.phone_number = phone_number or ""
            user.save() 

        else :
            if not first_name :
                first_name = ""

            if not last_name :
                last_name = ""
            
            if not location :
                location = ""

            if not username :
                username = ""

            if not phone_number :
                phone_number = ""

            TelegramUsers.objects.create(chat_id=chat_id, last_name=last_name, first_name=first_name,location=location, username=username, phone_number=phone_number)

    except :
        if not first_name :
            first_name = ""

        if not last_name :
            last_name = ""
        
        if not location :
            location = ""

        if not username :
            username = ""

        if not phone_number :
            phone_number = ""

        TelegramUsers.objects.create(chat_id=chat_id, last_name=last_name, first_name=first_name,location=location, username=username, phone_number=phone_number)

    with open("chat_ids.txt", "+a") as file :
        file.write(f"{chat_id} \n")

def createPost(request):
    content = request.POST.get("content")
    chat_id = request.POST.get("chat_id")
    context = request.POST.get("context") or "friend"
    user = TelegramUsers.objects.filter(chat_id=chat_id).first()

    if not user :
        return HttpResponse("Poster does not Exist")
    
    else :
        Posts.objects.create(content=content, telegram=user, target=context )
        return HttpResponse("Post Successfully Created")
    
def share_post(request, post_id):
    post_id = request.POST.get("post_id")
    original_post = request.POST.get(Posts, id=post_id)
    shared_at = request.POST.get("shared_at")
    shared_by = request.POST.get("shared_by")
    sharedpost = Posts.objects.create(user=request.user, content=original_post.content, shared_from=original_post, shared_at=shared_at, shared_by=shared_by)

    if sharedpost:
        return HttpResponse("post_list")
    
    else:
        return HttpResponse("Can't share post")
    

def topup(request):
    chat_id = request.POST.get("chat_id")
    payload = request.POST.get("payload")
    title = request.POST.get("title")
    description = request.POST.get("description")
    email = request.POST.get("email")
    name = request.POST.get("name")
    phone_number = request.POST.get("phone_number")
    shipping_address = request.POST.get("shipping_address")
    currency = request.POST.get("currency")
    price = request.POST.get("price")
    

    topup = Topup.objects.create(chat_id=chat_id, payload=payload, title=title, description=description, email=email, name=name, phone_number=phone_number, shipping_address=shipping_address, currency=currency, price=price ) 

    if  topup :
        return HttpResponse("Topup Successful")
    else:
        return HttpResponse("Topup Failed")



#model view template kind of framework
