from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    image_url = models.CharField(max_length=256, blank=True)
    category = models.CharField(max_length=64, blank=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.user_id} with starting price of {self.starting_bid}"


class Bid(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listing")
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user_id} bid {self.bid} on {self.listing_id}"


class Comment(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter")
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.user_id} commented {self.comment} on {self.listing_id}"


class Watchlist(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watcher")
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="watched")

    def __str__(self):
        return f"{self.user_id} is watching {self.listing_id}"
