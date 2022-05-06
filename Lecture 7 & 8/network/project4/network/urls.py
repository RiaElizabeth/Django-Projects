from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("editpost/<int:id>", views.editpost, name="editpost"),
    path("change/<int:id>", views.like_unlike, name="likepost"),
    path("profile/<str:username>",views.profile,name="profile"),
    path("following",views.following,name="following")
]
