from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("activelistings", views.activelistings, name="activelistings"),
    path("viewlisting/<int:product_id>", views.viewlisting, name="viewlisting"),
    path("cmntsubmit/<int:listingid>",views.cmntsubmit,name="cmntsubmit"),
    path("categories", views.categories, name="categories"),
    path("category/<str:categ>", views.category, name="category"),
    path("bidsubmit/<int:listingid>",views.bidsubmit,name="bidsubmit"),
    path("biderror", views.biderror, name="biderror"),
    path("closebid/<int:listingid>", views.closebid, name="closebid"),
    path("addtowatchlist/<int:product_id>",views.addtowatchlist,name="addtowatchlist"),
    path("watchlist/<str:username>",views.watchlist,name="watchlist"),

]
