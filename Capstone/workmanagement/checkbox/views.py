from datetime import date
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.contrib import messages
import json

from .models import Team, User, Task, Workflow

# Create your views here.

def index(request):
    if request.method == "POST":
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            assigned_by_tasks = []
            assigned_to_tasks = []
            tasks_all = Task.objects.all()
            for t in tasks_all:
                if t.assigned.filter(username=request.user.username):
                    assigned_to_tasks.append(t)
                if t.assignee.filter(username=request.user.username):
                    assigned_by_tasks.append(t)
            return render(request, "checkbox/homepage.html", {
                "assigned_by":assigned_by_tasks,
                "assigned_to": assigned_to_tasks
            })
        else:
            return render(request, "checkbox/index.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "checkbox/index.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        if User.objects.get(username=username):
            return render(request, "checkbox/register.html", {
                "message": "Username already exists."
            })
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "checkbox/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "checkbox/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "checkbox/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def home(request):
    assigned_by_tasks = []
    assigned_to_tasks = []
    tasks_all = Task.objects.all()
    for t in tasks_all:
        if t.assigned.filter(username=request.user.username):
            assigned_to_tasks.append(t)
        if t.assignee.filter(username=request.user.username):
            assigned_by_tasks.append(t)
    return render(request, "checkbox/homepage.html", {
            "assigned_by":assigned_by_tasks,
            "assigned_to": assigned_to_tasks
        })

def display_users(request):
    users = User.objects.all()
    return render(request, "checkbox/users.html", {
        "users":users
    })

def display_teams(request):
    teams_view = []
    teams = Team.objects.all()
    for t in teams:
        if t.user.filter(username=request.user.username):
            teams_view.append(t)
    return JsonResponse([team.serialize() for team in teams_view], safe=False)

def teams_menu(request):
    return render(request, "checkbox/teams.html")

def tasks(request):
    if request.method=="POST":
        title = request.POST["title"]
        assigned = request.POST.getlist("members")
        date = request.POST["date"]
        description = request.POST["description"]
        t = Task.objects.create()
        t.title = title
        t.due = date
        t.description = description
        t.assignee.add(User.objects.get(username=request.user.username))
        for a in assigned:
            u = User.objects.get(username=a)
            t.assigned.add(u)
        t.save()
        assigned_by_tasks = []
        assigned_to_tasks = []
        tasks_all = Task.objects.all()
        for t in tasks_all:
            if t.assigned.filter(username=request.user.username):
                assigned_to_tasks.append(t)
            if t.assignee.filter(username=request.user.username):
                assigned_by_tasks.append(t)
        return render(request, "checkbox/homepage.html", {
            "message": 1,
            "assigned_by":assigned_by_tasks,
            "assigned_to": assigned_to_tasks
        })
    return render(request, "checkbox/tasks.html", {
        "users": User.objects.all()
    })

def workflow(request):
    teams = []
    for t in Team.objects.all():
        if t.user.filter(username=request.user.username).count()>0:
            teams.append(t)
    tasks = []
    for task in Task.objects.all():
        if task.completed==False:
            tasks.append(task)
    if request.method=="POST":
        title = request.POST["workflow"]
        teams = request.POST.getlist("teams")
        tasks = request.POST.getlist("tasks")
        w = Workflow.objects.create()
        w.title = title
        for t in teams:
            tobj = Team.objects.get(id=t)
            w.team.add(tobj)
        for t in tasks:
            tobj = Task.objects.get(id=t)
            w.task.add(tobj)
        w.save()
        wfs = []
        for wf in Workflow.objects.all():
            if wf.team.filter(id=request.user.id).count()>0:
                wfs.append(wf)
        return render(request, "checkbox/assigned.html", {
            "message": 2,
            "workflows":wfs
        })
    return render(request, "checkbox/workflow.html", {
        "teams":teams,
        "tasks":tasks
    })

def create(request):
    users = User.objects.all()
    if request.method=="GET":
        return render(request, "checkbox/create.html",
        {"users":users})
    if request.method=="POST":
        title = request.POST["title"]
        members = request.POST.getlist("members")
        # return HttpResponse(members)
        if Team.objects.filter(title=title).count() >0:
            return render(request, "checkbox/create.html",
                {
                    "users":users,
                    "present":1
                })
        else:
            Team.objects.create(title=title)
            u = User.objects.get(username=request.user.username)
            Team.objects.get(title=title).user.add(u)
            Team.objects.get(title=title).owner.add(u)
            for mem in members:
                u = User.objects.get(username=mem)
                Team.objects.get(title=title).user.add(u)
        return render(request,"checkbox/teams.html", {
            "present":1
        })

def current_user(request):
    return JsonResponse({
        "current_user": request.user.username
    })

def editteam(request, id):
    if request.method == "POST":
        team = Team.objects.get(id=id)
        team.title = request.POST["title"]
        team.save()
        members = request.POST.getlist("members")
        Team.objects.get(id=id).user.clear()
        for m in members:
            usmem = User.objects.get(username=m)
            Team.objects.get(id=id).user.add(usmem)
        return HttpResponseRedirect(reverse('teams'))
    team = Team.objects.get(id=id)
    user_db = User.objects.all()
    team_users = team.user.all()
    us = []
    for u in user_db:
        if u not in team_users:
            us.append(u)
    return render(request, "checkbox/editteam.html", {
        "title": team.title,
        "users": team.user.all(),
        "user_remaining": us,
        "id": id 
    })

def update(request, id):
    if Task.objects.get(id=id).completed==False:
        Task.objects.filter(id=id).update(completed=True)
    else:
        Task.objects.filter(id=id).update(completed=False)
    return JsonResponse({
        "message":"Successfully updated!"
    })

def view_workflow(request):
    wfs = []
    for wf in Workflow.objects.all():
        if wf.team.filter(id=request.user.id).count()>0:
            wfs.append(wf)
    return render(request, "checkbox/assigned.html", {
        "workflows":wfs
    })