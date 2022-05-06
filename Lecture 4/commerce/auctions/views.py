from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Auction, Bid, Comment, Watchlist

def index(request):
    listings = Auction.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method=="POST":
        new_auc = Auction()
        new_auc.user = User.objects.get(username=request.POST["username"])
        new_auc.title = request.POST["title"]
        new_auc.description = request.POST["description"]
        new_auc.starting = request.POST["starting"]
        new_auc.image = request.POST["url"]
        new_auc.category = request.POST["categories"]
        new_auc.save()
        b = Bid()
        b.user = User.objects.get(username=request.POST["username"])
        b.auction = new_auc
        b.new_bid = request.POST["starting"]
        b.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html")

def categories(request):
    category = Auction.objects.order_by().values('category').distinct()
    return render(request, "auctions/categories.html", {
        "categories":category
    })

def category(request,group):
    items = Auction.objects.filter(category=group)
    return render(request, "auctions/index.html", {
        "listings": items
    })
    
@login_required
def item(request, item_name):
    item = Auction.objects.get(title=item_name)
    bids = Bid.objects.get(auction=item)
    message = ""
    comments = Comment.objects.filter(item=item)
    if request.method=="POST":
        val = float(request.POST["bid"])
        if val>bids.new_bid:
            bids.count = bids.count+1
            bids.save()
            user = User.objects.get(username=request.user.username)
            Bid.objects.filter(auction=item).update(new_bid=val)
            Bid.objects.filter(auction=item).update(user=user)
            bids = Bid.objects.get(auction=item)
            message = "Bid placed successfully."
        else:
            message = "The amount must be greater than the last bid."
    if item.active:
        won = False
    else:
        if request.user.username==bids.user.username:
            won = True
        else:
            won=False
    if item.user.username == request.user.username:
        close = True
    else:
        close = False
    try:
        if Watchlist.objects.get(item=item,user=User.objects.get(username=request.user.username)):
                w=True
    except Watchlist.DoesNotExist:
            w=False
    
    return render(request, "auctions/pages.html", {
        "item":item,
        "bids": bids.count,
        "price":bids.new_bid,
        "message":message,
        "close":close,
        "won":won,
        "comments":comments,
        "w":w
    })

def close(request, item_name):
    if request.method=="POST":
        Auction.objects.filter(title=item_name).update(active=False)
        item = Auction.objects.get(title=item_name)
        val = Bid.objects.get(auction=item)
        return render(request, "auctions/close.html", {
            "val":val.new_bid
        })
    return HttpResponse("<h1>Error!</h1>")

def comment(request, item_name):
    if request.method=="POST":
        c = Comment()
        c.user = User.objects.get(username=request.user.username)
        c.item = Auction.objects.get(title=item_name)
        c.new_comment = request.POST["comment"]
        c.save()
        return HttpResponseRedirect(reverse("item", args=[item_name,]))

def watchlist(request, item_name):
    item = Auction.objects.get(title=item_name)
    try:
        u = User.objects.get(username=request.user.username)
        w = Watchlist.objects.get(item=item, user=u)
        w.delete()
    except:
        w = Watchlist()
        w.user = User.objects.get(username=request.user.username)
        w.item = item
        w.save()
    return HttpResponseRedirect(reverse("item", args=[item_name,]))

def wishlist(request):
    user = User.objects.get(username=request.user.username)
    entries = Watchlist.objects.filter(user=user)
    count = entries.count()
    return render(request, "auctions/watchlist.html", {
        "listings": entries,
        "count":count
    })