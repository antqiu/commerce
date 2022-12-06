from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "auctions/index.html",
                  {"listings": Listing.objects.all()})


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


def categories(request):
    categories = []
    for category in Listing.objects.all():
        categories.append(category.category)
    categories = set(categories)
    return render(request, "auctions/categories.html", {"categories": categories, "listings": Listing.objects.all()})


def category(request, category):
    return render(request, "auctions/category.html", {"category": category, "listings": Listing.objects.filter(category=category)})


@login_required(login_url='/login')
def listing(request, listing_id):
    bids = Bid.objects.filter(listing_id=listing_id)
    bid_count = len(bids)
    highest_bid = Listing.objects.get(pk=listing_id).starting_bid
    highest_bidder = Listing.objects.get(pk=listing_id).user_id
    for bid in bids:
        if bid.bid > highest_bid:
            highest_bid = bid.bid
            highest_bidder = bid.user_id
        else:
            # bids.delete(bid)
            pass
    comments = Comment.objects.all().filter(listing_id=listing_id)

    if request.method == "POST":
        # print("posted!")
        if 'close' in request.POST:
            # print("closed!")
            listing = Listing.objects.get(id=listing_id)
            listing.active = False
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        if 'comment' in request.POST:
            comment = request.POST["comment"]
            newComment = Comment(user_id=request.user, listing_id=Listing.objects.get(
                pk=listing_id), comment=comment)
            newComment.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

        # handles bidding
        # handles if thhe bid price is lower than the current highest bid
        if 'bid' in request.POST:
            if int(request.POST["bid"]) < int(highest_bid):
                # sends the user back to the listing page with an error message
                return render(request, "auctions/listing.html", {
                    "message": "Bid must be higher than starting bid",
                    "listing": Listing.objects.get(id=listing_id),
                    "bids": Bid.objects.filter(listing_id=listing_id),
                    "bid_count": bid_count,
                    "highest_bid": highest_bid,
                    "comments": comments,
                    "highest_bidder": highest_bidder})
        # handles if the bid price is higher than the current bid
        # adds to the Bid database and saves it, returns the user to the listing page
            listing = Listing.objects.get(pk=listing_id)
            bid = Bid(user_id=request.user, listing_id=listing,
                      bid=request.POST["bid"])
            bid.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    # goes here if there is no post request, just displaying page regularly
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listing_id),
        "bids": Bid.objects.filter(listing_id=listing_id),
        "bid_count": bid_count,
        "highest_bid": highest_bid,
        "comments": comments,
        "highest_bidder": highest_bidder})


def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.POST["image_url"]
        category = request.POST["category"]
        newListing = Listing(user_id=request.user, title=title, description=description,
                             starting_bid=starting_bid, image_url=image, category=category)
        newListing.save()
        return HttpResponseRedirect(reverse("listing", args=(newListing.id,)))
    # regularly displays the page
    return render(request, "auctions/create.html")


def watchlist(request):
    if request.method == 'POST':
        user_id = request.POST["user_id"]
        user = User.objects.get(pk=user_id)
        listing_id = request.POST["listing_id"]
        listing = Listing.objects.get(pk=listing_id)
        # sees if watchlist already exists, if so removes and returns to the active listing page
        if Watchlist.objects.filter(user_id=user, listing_id=listing).exists():
            Watchlist.objects.filter(user_id=user, listing_id=listing).delete()
            return HttpResponseRedirect(reverse("index"))
        # add to the user's watchlist and return their own watchlist
        Watchlist.objects.create(user_id=user, listing_id=listing)
        return HttpResponseRedirect(reverse("watchlist"))
    watchlist = Watchlist.objects.filter(user_id=request.user)
    return render(request, "auctions/watchlist.html", {"watchlists": watchlist})
