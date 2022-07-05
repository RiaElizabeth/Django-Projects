from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("register", views.register, name='register'),
    path("logout", views.logout_view, name='logout'),
    path("home", views.home, name='home'),
    path("users", views.display_users, name='users'),
    path("teams", views.teams_menu, name='teams'),
    path("tasks", views.tasks, name='tasks'),
    path("workflow", views.workflow, name='workflow'),
    path("view_workflows",views.view_workflow, name='view_workflow'),
    path("create", views.create, name='create'),
    path("display_teams", views.display_teams, name='display_teams'),
    path("current_user", views.current_user, name='current_user'),
    path("editteam/<int:id>", views.editteam, name='editteam'),
    path("update/<int:id>", views.update, name='update')
]