from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("category/<str:group>", views.category, name="category"),
    path("listing/<str:item_name>", views.item, name="item"),
    path("<str:item_name>/close", views.close, name="close"),
    path("listing/<str:item_name>/comment", views.comment, name="comment"),
    path("listing/<str:item_name>/watchlist", views.watchlist, name="watchlist"),
    path("/wishlist", views.wishlist, name="wishlist")
]
