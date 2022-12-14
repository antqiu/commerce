from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("create", views.create, name="create"),
    path('watchlist', views.watchlist, name="watchlist"),
]
