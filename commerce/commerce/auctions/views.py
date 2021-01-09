from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    return render(request, "auctions/index.html")


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
def createlisting(request):
    if request.method == "POST":
        listing = Listing()
        listing.name = request.POST.get('name')
        listing.category = request.POST.get('category')
        listing.startingbid = request.POST.get('startingbid')
        listing.description = request.POST.get('description')
        listing.creator = request.user.username
        if request.POST.get('image'):
            listing.image = request.POST.get('image')
        else:
            listing.image = "https://www.brdtex.com/wp-content/uploads/2019/09/no-image-480x480.png"
        listing.save()
        allitems = Listing.objects.all()
        return render(request, "auctions/activelistings.html", {
            "allitems": allitems
        })
    else:
        return render(request, "auctions/createlisting.html")


def activelistings(request):
    allitems = Listing.objects.all()
    noitems = False
    if len(allitems) == 0:
        noitems = True
    return render(request, "auctions/activelistings.html", {
        "allitems": allitems,
        "noitems": noitems
    })


def viewlisting(request, product_id):
    listing = Listing.objects.get(id = product_id)
    comments = Comment.objects.filter(listingid=product_id)
    return render(request, "auctions/viewlisting.html", {
        "listing": listing,
        "comments": comments,
    })


def categories(request):
    return render(request, "auctions/categories.html")


def category(request, categ):
    categ_products = Listing.objects.filter(category=categ)
    return render(request, "auctions/category.html", {
        "categ": categ,
        "allitems": categ_products
    })


@login_required
def cmntsubmit(request,listingid):
    if request.method == "POST":
        c = Comment()
        c.comment = request.POST.get('comment')
        c.user = request.user.username
        c.listingid = listingid
        c.save()
        return redirect('viewlisting', product_id=listingid)
    else :
        return redirect('index')


@login_required
def biderror(request):
    return render(request, "auctions/biderror.html")

@login_required
def bidsubmit(request,listingid):
    current_bid = Listing.objects.get(id=listingid)
    current_bid=current_bid.startingbid
    if request.method == "POST":
        user_bid = int(request.POST.get("bid"))
        if user_bid > current_bid:
            listing_items = Listing.objects.get(id=listingid)
            listing_items.startingbid = user_bid
            listing_items.save()
            return redirect('viewlisting', product_id=listingid)
        else:
            return render(request, "auctions/biderror.html",{
                "listing": listingid
            })


@login_required
def closebid(request, listingid):
    if request.user.username:
        try:
            listingrow = Listing.objects.get(id=listingid)
        except:
            return redirect('index')
        cb = Closedbid()
        cb.owner = listingrow.creator
        cb.listingid = listingid
        try:
            bidrow = Bid.objects.get(listingid=listingid,bid=listingrow.startingbid)
            cb.winner = bidrow.user
            cb.winprice = bidrow.bid
            cb.save()
            bidrow.delete()
        except:
            cb.winner = listingrow.creator
            cb.winprice = listingrow.startingbid
            cb.save()
        listingrow.delete()
        return render(request, "auctions/closedlisting.html",{
            "closedbid": cb,
            "listing": listingrow
        })


@login_required
def addtowatchlist(request, product_id):

    obj = Watchlist.objects.filter(
        listingid=product_id, user=request.user.username)
    comments = Comment.objects.filter(listingid=product_id)
    # checking if it is already added to the watchlist
    if obj:
        # if its already there then user wants to remove it from watchlist
        obj.delete()
        # returning the updated content
        product = Listing.objects.get(id=product_id)
        added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username)
        return render(request, "auctions/viewlisting.html", {
            "listing": product,
            "added": added,
            "comments": comments
        })
    else:
        # if it not present then the user wants to add it to watchlist
        obj = Watchlist()
        obj.user = request.user.username
        obj.listingid = product_id
        obj.save()
        # returning the updated content
        product = Listing.objects.get(id=product_id)
        added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username)
        return render(request, "auctions/viewlisting.html", {
            "listing": product,
            "added": added,
            "comments": comments
        })

@login_required
def watchlist(request,username):
    if request.user.username:
        try:
            w = Watchlist.objects.filter(user=username)
            items = []
            for i in w:
                items.append(Listing.objects.filter(id=i.listingid))
            try:
                w = Watchlist.objects.filter(user=request.user.username)
                wcount=len(w)
            except:
                wcount=None
            return render(request,"auctions/watchlist.html",{
                "items":items,
                "wcount":wcount
            })
        except:
            try:
                w = Watchlist.objects.filter(user=request.user.username)
                wcount=len(w)
            except:
                wcount=None
            return render(request,"auctions/watchlist.html",{
                "items":None,
                "wcount":wcount
            })
    else:
        return redirect('index')
