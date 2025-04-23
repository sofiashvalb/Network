from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

from .models import User, Post, Follow


def index(request):
    posts = Post.objects.all().order_by("id").reverse()
    
    paginator = Paginator(posts, 10)
    pageNum = request.GET.get('page')
    posts_per_page = paginator.get_page(pageNum)

    return render(request, "network/index.html", {
        "posts":posts,
        "posts_per_page":posts_per_page
    })

def likedPost(request, post_id):
    liked = False
    if request.method == "POST" and request.user.is_authenticated:
        post = Post.objects.get(id=post_id)

        if request.user in post.liked.all():
            #Then unlike
            post.liked.remove(request.user)
            liked = False
        else:
            #like
            post.liked.add(request.user)
            liked = True

    return JsonResponse({"liked":liked, "likeCount":post.liked.count()})

def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        newPost = Post.objects.get(pk=post_id)
        newPost.content = data["content"]
        newPost.save() 

        return JsonResponse({"message":"Changed", "data": data["content"]}) 


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user).order_by("id").reverse()
    
    # who the user follows
    following = Follow.objects.filter(user=user)

    # who follows the user
    followers = Follow.objects.filter(user_follower=user)

    try:
        check = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(check) != 0:
            isFollow = True
        else:
            isFollow = False
    except:
        isFollow = False


    paginator = Paginator(posts, 10)
    pageNum = request.GET.get('page')
    posts_per_page = paginator.get_page(pageNum)
     

    return render(request, "network/profile.html", {
        "posts":posts,
        "posts_per_page":posts_per_page,

        # comes from the django User model 
        "username":user.username, 
        "following":following,
        "followers":followers,
        "isFollow":isFollow, 
        "user_profile":user
    }) 

def following(request):
    user = User.objects.get(pk=request.user.id)
    
    following = Follow.objects.filter(user=user)
    followed_users = [f.user_follower for f in following]
    posts = Post.objects.filter(user__in=followed_users).order_by("id").reverse()

    paginator = Paginator(posts, 10)
    pageNum = request.GET.get('page')
    posts_per_page = paginator.get_page(pageNum)
     

    return render(request, "network/following.html", {
        "posts_per_page":posts_per_page,
    })

def follow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    followdata = User.objects.get(username=userfollow)
    f = Follow(user=currentUser, user_follower=followdata)
    f.save()
    user_id = followdata.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))

def unfollow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    followdata = User.objects.get(username=userfollow)
    f = Follow.objects.get(user=currentUser, user_follower=followdata)
    f.delete()
    user_id = followdata.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))

def newPost(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))
    
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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
