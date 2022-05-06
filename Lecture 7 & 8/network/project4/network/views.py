from cgitb import text
from dis import dis
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from requests import post

from .models import User, Post, Like, Follower


def index(request):
    l=[]
    all_posts = Post.objects.all().order_by('-date')
    for ap in all_posts:
        for f in ap.liked.all():
            if f.id == request.user.id:
                l.append(ap.id)
    paginator = Paginator(all_posts,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts":page_obj,
        "liked": l
    })

def newpost(request):
    if request.method=="POST":
        user = request.user.username
        post_user = User.objects.get(username=user)
        content = request.POST["content"]
        post = Post.objects.create(user=post_user, content=content)
        return HttpResponseRedirect(reverse('index'))
    return render(request, "network/newpost.html")

def editpost(request, id):
    post = Post.objects.get(id=id)
    if post.user.id != request.user.id:
        return HttpResponse("<br><br><h3>Forbidden request. You can only edit your own posts.</h3>")
    if request.method=="POST":
        post.content = request.POST["content"]
        post.save()
        return HttpResponseRedirect(reverse('index'))
    if request.method=="PUT":
        content = json.loads(request.body)
        post.content = content.get("content")
        post.save()
        return JsonResponse({"content":post.content})
    return render(request, "network/editpost.html", {
        "post":post
    })
    
def like_unlike(request,id):
    user = User.objects.get(username=request.user.username)
    post = Post.objects.get(id = id)
    if request.method=="POST":
        try:
            post.liked.get(id=user.id)
            post.liked.remove(user)
            count = Post.objects.get(id=id).liked.count()
            return JsonResponse({"text":"Like",
            "count": count})
        except:
            post.liked.add(user)
            count = Post.objects.get(id=id).liked.count()
            return JsonResponse({"text":"Unlike",
            "count": count})
    return HttpResponse("Success")

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
            follower = Follower.objects.create(username=user)
            follower.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request,username):
    user = User.objects.get(username=username)
    profile = Follower.objects.get(username=user)
    user_posts = Post.objects.filter(user=user)
    display = True
    text = ""
    if request.method == "POST":
        try:
            using = User.objects.get(username=request.user.username)
            profile.follower.get(username = using)
            profile.follower.remove(using)
            profile = Follower.objects.get(username=user)
            return JsonResponse({"text":"Follow",
            "follower":profile.follower.count(),
            "following":profile.following.count()})
        except:
            user_here = User.objects.get(username=request.user.username)
            profile.follower.add(user_here)
            profile = Follower.objects.get(username=user)
            return JsonResponse({"text":"Unfollow",
            "follower":profile.follower.count(),
            "following":profile.following.count()})
    if(request.user.username==username):
        display = False
    else:
        try:
            profile.follower.get(username=request.user.username)
            text = "Unfollow"
        except:
            text = "Follow"
    return render(request,"network/profile.html", {
        "username":username,
        "profile":profile,
        "user_posts": user_posts,
        "display":display,
        "text":text
    })

def following(request):
    l=[]
    user = User.objects.get(username=request.user.username)
    following = Follower.objects.get(username=user).follower.all()
    all_posts = Post.objects.all()
    for f in following:
        for p in all_posts:
            if f.id==p.user.id:
                l.append(p)
    paginator = Paginator(l,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"network/following.html", {
        "all_posts":page_obj
    })

# from django.db.models import Q
# Post.objects.filter(Q(user=admin)|Q(user=user1))
