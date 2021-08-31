from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from datetime import datetime
from datetime import date
from django.core import serializers
from django.core.paginator import Paginator
from .models import User,Posts,Following,Likes


def index(request):
    return render(request, "network/index.html")

def following_index(request):
    return render(request, "network/following.html")
def following(request):
     #Getting the User
    user = request.user
    #This is the code that will allow us to create posts.
    if request.method =="POST":
        post = request.POST["content"]
        
        new_post = Posts(user = user, post = post)
        new_post.save()

        #Redirect User to Index
        return HttpResponseRedirect(reverse("index"))

   
   #This is the code that will let us access our posts.
    if request.method == "GET":

        #Getting  queryset count so that we can update the end variable
        #accordingly
        total_posts =Posts.objects.count()
        #Getting start and end points
        start = int(request.GET.get("start") or 0)
        end = int(request.GET.get("end") or (start + 9))
        
        #Getting all of the Posts
        posts = Posts.objects.all()


        #ordering them by timestamp
        posts = posts.order_by("-date").all()

       
       

        #Generating a list of posts.
        #For it to work I first get the value of the queryset
        #and convert it to a list, once it is a list item, I convert
        #it to a string so that I can slice it accordingly since
        # you can't pass a query set as a argument for a JSon Response
        data =[]
        for x in range(start,total_posts):
            ##Here I'm getting the username of the user who created the post
            #by getting the user that matches the id since in my post model
            #user was a foreign key.
            
            post_user_id = posts[x].user.id
            post_user = User.objects.filter(pk= post_user_id)
            post_date = posts[x].date

            #If the value of x exceeds the number of posts we have
            #in the database it doesnt make sense for us to keep
            #looping and trt to get more stuff.
            if x+1 > total_posts:
                break

            if posts[x] != None:
                #converting date to a valid format ('YYYY-MM-DDTHH:MM')
                post_date =post_date.strftime("%Y-%m-%dT%H:%M")
                post_date=list(post_date)
                
               
                #changing commas to dashes
                post_date[4]= "-"
                post_date[7]= "-"
                #Making sure that if we have a month or date below that starts with
                #0 we add a zero cause it would be like 6 instead of 06
                if post_date[9] ==",":
                    post_date =  post_date[:8] +["0"]+ post_date[8:]
                
                
                #modifying specific characters
                post_date[10]= "T"
                post_date[13]=":"
                #changing whitespace to 0
                for i in range(len(post_date)):
                    if post_date[i] == " ":
                        post_date[i] = "0"
                #if a time starts with 0 and follows a comma it means that it was 00
                #therefore we substitute
                if post_date[14]=="0" and post_date[15] ==",":
                    post_date[15]="0"
                if post_date[14]>"0" and post_date[15] ==",":
                    post_date[15]=post_date[14]
                    post_date[14]="0"
                if post_date[14]=="," and int(post_date[13])>0:
                    post_date[14]=post_date[13]
                    post_date[13]="0"
                #trimming   
                if len(post_date)>16:
                    post_date = post_date[:-1] 
                
                new_date = ""
                new_date = new_date.join(post_date)
                
        
            ##Getting the number of likes
            likes = posts[x].likes
            
            
            post ={
                'user':str(post_user)[18:-3],
                'post':str(posts[x].post),
                'date':new_date,
                'likes':str(likes),
                'id':int(posts[x].id),
                'image':str(post_user[0].profile_pic)
            }
            #here we check if the post is from one of the users the current user follows
            #if it is we append the post, if not we dont.
            follows = Following.objects.all()
            for x in follows:
                if(x.user.username == user.username and str(post_user)[18:-3] == x.following.username):
                    data.append(post)
                    

        
        #Paginator Code
        paginator = Paginator(data,10)
        page_number = request.GET.get('page')
        page_obj= paginator.get_page(page_number)
        end = len(page_obj.object_list)
        posts = page_obj.object_list
        totalpages = paginator.num_pages  

        

        likes = Likes.objects.all()
        likes_array =[]
        for x in likes:
                new_like ={
                    'user':x.user.id,
                    'post':x.post.id
                }
                likes_array.append(new_like) 

        #Getting the number of people the user follows and the number of people who follow the user.
        following = 0
        followers = 0
        follows = Following.objects.all()
        for x in follows:
            if x.user.username == user.username:
                following +=1
            if x.following.username == user.username:
                followers +=1
        

        #Getting the User
        user = request.user           
        #returning lists of posts
        return JsonResponse({
            "posts":posts,
            "likes":likes_array,
            "user":user.id,
            "username":user.username,
            "user_image":str(user.profile_pic),
            "following":following,
            "followers":followers,
            "totalpages":round(len(data)/10),
            "currentpage":page_number
            
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        image= request.POST["img"]
        

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            current_user = User.objects.filter(username =username).update(profile_pic=image)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def post(request):
     #Getting the User
    user = request.user
    #This is the code that will allow us to create posts.
    if request.method =="POST":
        post = request.POST["content"]
        
        new_post = Posts(user = user, post = post)
        new_post.save()

        #Redirect User to Index
        return HttpResponseRedirect(reverse("index"))

   
   #This is the code that will let us access our posts.
    if request.method == "GET":
        #Getting  queryset count so that we can update the end variable
        #accordingly
        total_posts = Posts.objects.count()
        
        #Getting start and end points
        start = 0
        end = 9
        
        #Getting all of the Posts
        posts = Posts.objects.all()

        #ordering them by timestamp
        posts = posts.order_by("-date").all()

        #Paginator Code
        paginator = Paginator(posts,10)
        page_number = request.GET.get('page')
        page_obj= paginator.get_page(page_number)
        end = len(page_obj.object_list)
        posts = page_obj.object_list
        totalpages = paginator.num_pages
       
        #Generating a list of posts.
        #For it to work I first get the value of the queryset
        #and convert it to a list, once it is a list item, I convert
        #it to a string so that I can slice it accordingly since
        # you can't pass a query set as a argument for a JSon Response
        data =[]
        for x in range(start ,end):
            ##Here I'm getting the username of the user who created the post
            #by getting the user that matches the id since in my post model
            #user was a foreign key.
            
            post_user_id = posts[x].user.id
            post_user = User.objects.filter(pk= post_user_id)
            post_date = posts[x].date

            #If the value of x exceeds the number of posts we have
            #in the database it doesnt make sense for us to keep
            #looping and trt to get more stuff.
            if x+1 > total_posts:
                break

            if posts[x] != None:
                #converting date to a valid format ('YYYY-MM-DDTHH:MM')
                post_date =post_date.strftime("%Y-%m-%dT%H:%M")
                post_date=list(post_date)
                
               
                #changing commas to dashes
                post_date[4]= "-"
                post_date[7]= "-"
                #Making sure that if we have a month or date below that starts with
                #0 we add a zero cause it would be like 6 instead of 06
                if post_date[9] ==",":
                    post_date =  post_date[:8] +["0"]+ post_date[8:]
                
                
                #modifying specific characters
                post_date[10]= "T"
                post_date[13]=":"
                #changing whitespace to 0
                for i in range(len(post_date)):
                    if post_date[i] == " ":
                        post_date[i] = "0"
                #if a time starts with 0 and follows a comma it means that it was 00
                #therefore we substitute
                if post_date[14]=="0" and post_date[15] ==",":
                    post_date[15]="0"
                if post_date[14]>"0" and post_date[15] ==",":
                    post_date[15]=post_date[14]
                    post_date[14]="0"
                if post_date[14]=="," and int(post_date[13])>0:
                    post_date[14]=post_date[13]
                    post_date[13]="0"
                #trimming   
                if len(post_date)>16:
                    post_date = post_date[:-1] 
                
                new_date = ""
                new_date = new_date.join(post_date)
                
        
            ##Getting the number of likes
            likes = posts[x].likes
            
            
            post ={
                'user':str(post_user)[18:-3],
                'post':str(posts[x].post),
                'date':new_date,
                'likes':str(likes),
                'id':int(posts[x].id),
                'image':str(post_user[0].profile_pic)
            }
            data.append(post)
           
        likes = Likes.objects.all()
        likes_array =[]
        for x in likes:
                new_like ={
                    'user':x.user.id,
                    'post':x.post.id
                }
                likes_array.append(new_like) 

        #Getting the User
        user = request.user           
        #returning lists of posts
        return JsonResponse({
            "posts":data,
            "likes":likes_array,
            "user":user.id,
            "username":user.username,
            "user_image":str(user.profile_pic),
            "totalpages":int(totalpages),
            "currentpage":int(page_number)
            
        })

def profile(request,user):
    return render(request, "network/user.html",{
        "username":user
    })


def user(request, user):
    #Profile Clicked on
    username = user
   #Getting the User
    user = request.user
    f = User.objects.get(username = username)

    #Getting start and end points
    start = 0
    end = 9
    #Getting  queryset count so that we can update the end variable
    #accordingly
    total_posts =Posts.objects.filter(user=f).count()
   #Getting the Posts
    posts = Posts.objects.filter(user=f)
    
    #ordering them by timestamp
    posts = posts.order_by("-date").all()

   

    #Paginator Code
    paginator = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj= paginator.get_page(page_number)
    end = len(page_obj.object_list)
    posts = page_obj.object_list
    totalpages = paginator.num_pages

   #Generating a list of posts.
    #For it to work I first get the value of the queryset
    #and convert it to a list, once it is a list item, I convert
    #it to a string so that I can slice it accordingly since
    # you can't pass a query set as a argument for a JSon Response
    data =[]
    for x in range(start ,end):
        ##Here I'm getting the username of the user who created the post
        #by getting the user that matches the id since in my post model
        #user was a foreign key.
        
        post_user_id = posts[x].user.id
        post_user = User.objects.filter(pk= post_user_id)
        post_date = posts[x].date

        #If the value of x exceeds the number of posts we have
        #in the database it doesnt make sense for us to keep
        #looping and trt to get more stuff.
        if x+1 > total_posts:
            break

        if posts[x] != None:
            #converting date to a valid format ('YYYY-MM-DDTHH:MM')
            post_date =post_date.strftime("%Y-%m-%dT%H:%M")
            post_date=list(post_date)
            
            
            #changing commas to dashes
            post_date[4]= "-"
            post_date[7]= "-"
            #Making sure that if we have a month or date below that starts with
            #0 we add a zero cause it would be like 6 instead of 06
            if post_date[9] ==",":
                post_date =  post_date[:8] +["0"]+ post_date[8:]
            
            
            #modifying specific characters
            post_date[10]= "T"
            post_date[13]=":"
            #changing whitespace to 0
            for i in range(len(post_date)):
                if post_date[i] == " ":
                    post_date[i] = "0"
            #if a time starts with 0 and follows a comma it means that it was 00
            #therefore we substitute
            if post_date[14]=="0" and post_date[15] ==",":
                post_date[15]="0"
            if post_date[14]>"0" and post_date[15] ==",":
                post_date[15]=post_date[14]
                post_date[14]="0"
            if post_date[14]=="," and int(post_date[13])>0:
                post_date[14]=post_date[13]
                post_date[13]="0"
            #trimming   
            if len(post_date)>16:
                post_date = post_date[:-1] 
            
            new_date = ""
            new_date = new_date.join(post_date)
            
    
        ##Getting the number of likes
        likes = posts[x].likes
        
        
        post ={
            'user':str(post_user)[18:-3],
            'post':str(posts[x].post),
            'date':new_date,
            'likes':str(likes),
            'id':int(posts[x].id),
            'image':str(post_user[0].profile_pic)
        }

        if str(list(post_user))[8:-2] == username:
            data.append(post)
            
    likes = Likes.objects.all()
    likes_array =[]
    for x in likes:
        new_like ={
            'user':x.user.id,
            'post':x.post.id
        }
        likes_array.append(new_like)

    
    #Creating a new array that will hold the value of the Following Table
    #So that we can check if the user follows a person or not using javascript
    follows = Following.objects.all()
    follows_array=[]
    for x in follows:
        new_follow ={
            'user':x.user.username,
            'following':x.following.username              
        }
        follows_array.append(new_follow)

    #Getting the number of people the user follows and the number of people who follow the user.
    following = 0
    followers = 0
    follows = Following.objects.all()
    for x in follows:
        if x.user.username == username:
            following +=1
        if x.following.username == username:
            followers +=1
        
    #returning lists of posts
    return JsonResponse({
        "posts":data,
        "likes":likes_array,
        "user":user.id,
        "user_image":str(user.profile_pic),
        "username":user.username,
        "follows":follows_array,
        "following":following,
        "followers":followers, 
        "totalpages":totalpages,
        "currentpage":page_number
    })

def like(request,id):

    
    # Getting the User
    user = request.user
    #Creating a list that will hold the user who liked the post
    #to see if we like or unlike the post.
    
    #We check if theres any likes already in our likes table
    #if not we create our first like.
    count = Likes.objects.count()

    if count == 0:
        #Getting the specific object that has a specific id for the likes
        post= Posts.objects.get(pk=id)
        #Updating the likes in the post itself
        post.likes = post.likes + 1
        new_user = User.objects.get(pk=user.id)
        #saving the likes
        Posts.objects.filter(pk=id).update(likes=post.likes)
        #Creating a new entry for our like database
        new_like= Likes(user = new_user, post = post)
        new_like.save()
    #if there are already likes in our table we need to check 
    #if the user already liked the post or not by looping through
    #the queryset. If found we have to decrement the like and delete it from
    #database, if not found we simply add a like
    else:
        found = False
        likes_ = Likes.objects.all()
        for x in likes_:
            # If found
            if x.user == user and x.post.id == id:
                found = True
                #Updating the likes in the post itself
                #Getting the specific object that has a specific id for the likes
                post= Posts.objects.get(pk=id)
                post.likes = post.likes - 1
                # # #saving the post
                
                Posts.objects.filter(pk=id).update(likes=post.likes)
                #Now we delete the like from our database
                x.delete()
        if found == False:
            #Getting the specific object that has a specific id for the likes
            post= Posts.objects.get(pk=id)
            #Updating the likes in the post itself
            post.likes = post.likes + 1
            new_user = User.objects.get(pk=user.id)
            #saving the likes
            Posts.objects.filter(pk=id).update(likes=post.likes)
            #Creating a new entry for our like database
            new_like= Likes(user = new_user, post = post)
            new_like.save() 


    #Recreating the specific post with updated data
    #so that we can update the div in javascript
    posts = Posts.objects.get(pk=id)
    post_user_id = Posts.objects.filter(pk=id).values('user')
    post_user_id =str(list(post_user_id))[9:-2]
    post_user = User.objects.get(pk= post_user_id)
    post_date = Posts.objects.filter(pk=id).values('date')

    #Code to fix the date
    #converting date to a valid format ('YYYY-MM-DDTHH:MM')
    post_date = str(list(post_date))[28:47]
    post_date = list(post_date)
    #Eliminating whitespace
    post_date = post_date[:8] + post_date[9:]
    post_date = post_date[:11] + post_date[12:]
    post_date = post_date[:14] + post_date[15:]
    #changing commas to dashes
    post_date[4]= "-"
    post_date[7]= "-"
    #Making sure that if we have a month or date below that starts with
    #0 we add a zero cause it would be like 6 instead of 06
    if post_date[9] ==",":
            post_date =  post_date[:8] +["0"]+ post_date[8:]
    
    
    #modifying specific characters
    post_date[10]= "T"
    post_date[13]=":"
    #changing whitespace to 0
    for i in range(len(post_date)):
        if post_date[i] == " ":
            post_date[i] = "0"
    #if a time starts with 0 and follows a comma it means that it was 00
    #therefore we substitute
    if post_date[14]=="0" and post_date[15] ==",":
        post_date[15]="0"
    if post_date[14]>"0" and post_date[15] ==",":
        post_date[15]=post_date[14]
        post_date[14]="0"
    if post_date[14]=="," and int(post_date[13])>0:
        post_date[14]=post_date[13]
        post_date[13]="0"
    #trimming   
    if len(post_date)>16:
        post_date = post_date[:-1] 
    
    new_date = ""
    new_date = new_date.join(post_date)
    
    post ={
        'user':str(post_user),
        'post':str(list(Posts.objects.filter(pk=id).values('post')))[11:-3],
        'date':new_date,
        'likes':posts.likes,
        'id':int(id),
        'image':str(post_user.profile_pic)
    }
    data =[] 
    data.append(post)
    #Code to create a likes aray that we will send using json
    likes = Likes.objects.all()
    likes_array =[]
    for x in likes:
        new_like ={
            'user':x.user.id,
            'post':x.post.id
        }
        likes_array.append(new_like)
    
    #returning lists of posts 
    return JsonResponse({
        "posts":data,
        "likes":likes_array,
        "user":user.id,
        "username":user.username
    })

def follow(request,id):
    
    # Getting the User
    current_user = request.user
    #Creating a list that will hold the user who liked the post
    #to see if we like or unlike the post.
    
    #Code to get the user that we want to follow 
    post= Posts.objects.get(pk=id)
    to_follow= User.objects.get(username=post.user) 

    #We check if theres any Follows already in our Following table
    #if not we create our first follow
    count = Following.objects.count()

    if count == 0:
        
        
        #Creating a new entry for our like database
        new_follow = Following(user = current_user, following = to_follow)
        new_follow.save()

    # If there are users already following each other in our table
    #We need to check if the user already follows the user that he clicked on
    #if it already follows it we unfollow and if it doesnt we follow.

    else:
        found = False
        follows = Following.objects.all()
        for x in follows:
            # If found
            if x.user == current_user and x.following == to_follow:
                found = True
                #We found that the current user already follows the other user therefore we unfollow by deleting the
                #entry in the database.
                x.delete()
        if found == False:
            
            #Creating a new entry for our like database
            new_follow = Following(user = current_user, following = to_follow)
            new_follow.save()


    #Recreating the specific post with updated data
    #so that we can update the div in javascript
    posts = Posts.objects.get(pk=id)
    post_user_id = Posts.objects.filter(pk=id).values('user')
    post_user_id =str(list(post_user_id))[9:-2]
    post_user = User.objects.get(pk= post_user_id)
    post_date = Posts.objects.filter(pk=id).values('date')

    #Code to fix the date
    #converting date to a valid format ('YYYY-MM-DDTHH:MM')
    post_date = str(list(post_date))[28:47]
    post_date = list(post_date)
    #Eliminating whitespace
    post_date = post_date[:8] + post_date[9:]
    post_date = post_date[:11] + post_date[12:]
    post_date = post_date[:14] + post_date[15:]
    #changing commas to dashes
    post_date[4]= "-"
    post_date[7]= "-"
    #Making sure that if we have a month or date below that starts with
    #0 we add a zero cause it would be like 6 instead of 06
    if post_date[9] ==",":
            post_date =  post_date[:8] +["0"]+ post_date[8:]
    
    
    #modifying specific characters
    post_date[10]= "T"
    post_date[13]=":"
    #changing whitespace to 0
    for i in range(len(post_date)):
        if post_date[i] == " ":
            post_date[i] = "0"
    #if a time starts with 0 and follows a comma it means that it was 00
    #therefore we substitute
    if post_date[14]=="0" and post_date[15] ==",":
        post_date[15]="0"
    if post_date[14]>"0" and post_date[15] ==",":
        post_date[15]=post_date[14]
        post_date[14]="0"
    if post_date[14]=="," and int(post_date[13])>0:
        post_date[14]=post_date[13]
        post_date[13]="0"
    #trimming   
    if len(post_date)>16:
        post_date = post_date[:-1] 
    
    new_date = ""
    new_date = new_date.join(post_date)
    
    post ={
        'user':str(post_user),
        'post':str(list(Posts.objects.filter(pk=id).values('post')))[11:-3],
        'date':new_date,
        'likes':posts.likes,
        'id':int(id),
        'image':str(post_user.profile_pic)
    }
    data =[] 
    data.append(post)

    likes = Likes.objects.all()
    likes_array =[]
    for x in likes:
        new_like ={
            'user':x.user.id,
            'post':x.post.id
        }
        likes_array.append(new_like)
    
    #Creating a new array that will hold the value of the Following Table
    #So that we can check if the user follows a person or not using javascript
    follows = Following.objects.all()
    follows_array=[]
    for x in follows:
        new_follow ={
            'user':x.user.username,
            'following':x.following.username              
        }
        follows_array.append(new_follow)

    #Getting the number of people the user follows and the number of people who follow the user.
    following = 0
    followers = 0
    follows = Following.objects.all()
    for x in follows:
        if x.user.username == to_follow.username:
            following +=1
        if x.following.username == to_follow.username:
            followers +=1
        
    #returning lists of posts 
    return JsonResponse({
        "posts":data,
        "likes":likes_array,
        "user":current_user.id,
        "username":current_user.username,
        "follows":follows_array,
        "second_user":to_follow.username,
        "following":following,
        "followers":followers
    })
    
def edit(request,id):

    if request.method == "GET":
        # Getting the User
        user = request.user
        #Getting the specific object that has a specific id for the likes
        post= Posts.objects.get(pk=id)

        #Recreating the specific post with updated data
        #so that we can update the div in javascript

        post_user_id = Posts.objects.filter(pk=id).values('user')
        post_user_id = str(list(post_user_id))[9:-2]
        post_user = User.objects.get(pk=post_user_id)
        post_date = Posts.objects.filter(pk=id).values('date')

        #Code to fix the date
        #converting date to a valid format ('YYYY-MM-DDTHH:MM')
        post_date = str(list(post_date))[28:47]
        post_date = list(post_date)
        #Eliminating whitespace
        post_date = post_date[:8] + post_date[9:]
        post_date = post_date[:11] + post_date[12:]
        post_date = post_date[:14] + post_date[15:]
        #changing commas to dashes
        post_date[4]= "-"
        post_date[7]= "-"
        #Making sure that if we have a month or date below that starts with
        #0 we add a zero cause it would be like 6 instead of 06
        if post_date[9] ==",":
                post_date =  post_date[:8] +["0"]+ post_date[8:]
        
        
        #modifying specific characters
        post_date[10]= "T"
        post_date[13]=":"
        #changing whitespace to 0
        for i in range(len(post_date)):
            if post_date[i] == " ":
                post_date[i] = "0"
        #if a time starts with 0 and follows a comma it means that it was 00
        #therefore we substitute
        if post_date[14]=="0" and post_date[15] ==",":
            post_date[15]="0"
        if post_date[14]>"0" and post_date[15] ==",":
            post_date[15]=post_date[14]
            post_date[14]="0"
        if post_date[14]=="," and int(post_date[13])>0:
            post_date[14]=post_date[13]
            post_date[13]="0"
        #trimming   
        if len(post_date)>16:
            post_date = post_date[:-1] 
        
        new_date = ""
        new_date = new_date.join(post_date)
        
        post ={
            'user':str(post_user),
            'post':str(list(Posts.objects.filter(pk=id).values('post')))[11:-3],
            'date':new_date,
            'likes':post.likes,
            'id':int(id),
            'image':str(post_user.profile_pic)
        }
        data =[] 
        data.append(post)
        likes = Likes.objects.all()
        likes_array =[]
        for x in likes:
            new_like ={
                'user':x.user.id,
                'post':x.post.id
            }
            likes_array.append(new_like)
        
        #returning lists of posts 
        return JsonResponse({
            "posts":data,
            "likes":likes_array,
            "user":user.id,
            "username":user.username
        })
def repost(request,id,new_post):

        # Getting the User
        user = request.user
        #Getting the specific object that has a specific id for the likes
        post= Posts.objects.get(pk=id)
        #updating the post
         #saving the likes
        Posts.objects.filter(pk=id).update(post=new_post)
        #Recreating the specific post with updated data
        #so that we can update the div in javascript

        post_user_id = Posts.objects.filter(pk=id).values('user')
        post_user_id = str(list(post_user_id))[9:-2]
        post_user = User.objects.get(pk=post_user_id)
        post_date = Posts.objects.filter(pk=id).values('date')

        #Code to fix the date
        #converting date to a valid format ('YYYY-MM-DDTHH:MM')
        post_date = str(list(post_date))[28:47]
        post_date = list(post_date)
        #Eliminating whitespace
        post_date = post_date[:8] + post_date[9:]
        post_date = post_date[:11] + post_date[12:]
        post_date = post_date[:14] + post_date[15:]
        #changing commas to dashes
        post_date[4]= "-"
        post_date[7]= "-"
        #Making sure that if we have a month or date below that starts with
        #0 we add a zero cause it would be like 6 instead of 06
        if post_date[9] ==",":
                post_date =  post_date[:8] +["0"]+ post_date[8:]
        
        
        #modifying specific characters
        post_date[10]= "T"
        post_date[13]=":"
        #changing whitespace to 0
        for i in range(len(post_date)):
            if post_date[i] == " ":
                post_date[i] = "0"
        #if a time starts with 0 and follows a comma it means that it was 00
        #therefore we substitute
        if post_date[14]=="0" and post_date[15] ==",":
            post_date[15]="0"
        if post_date[14]>"0" and post_date[15] ==",":
            post_date[15]=post_date[14]
            post_date[14]="0"
        if post_date[14]=="," and int(post_date[13])>0:
            post_date[14]=post_date[13]
            post_date[13]="0"
        #trimming   
        if len(post_date)>16:
            post_date = post_date[:-1] 
        
        new_date = ""
        new_date = new_date.join(post_date)
        
        post ={
            'user':str(post_user),
            'post':str(list(Posts.objects.filter(pk=id).values('post')))[11:-3],
            'date':new_date,
            'likes':post.likes,
            'id':int(id),
            'image':str(post_user.profile_pic)
        }
        data =[] 
        data.append(post)
        likes = Likes.objects.all()
        likes_array =[]
        for x in likes:
            new_like ={
                'user':x.user.id,
                'post':x.post.id
            }
            likes_array.append(new_like)
        
        #returning lists of posts 
        return JsonResponse({
            "posts":data,
            "likes":likes_array,
            "user":user.id,
            "username":user.username
        })
