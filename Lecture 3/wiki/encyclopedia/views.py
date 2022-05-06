from django.shortcuts import render
import markdown
from django.http import HttpResponse
from django import forms
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.urls import reverse
import random


from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    if util.get_entry(title)==None:
        content = "<h1>Requested page not found</h1><br><br><p>The title asked for does not exist. If you have adequate information, please consider creating the page."
        flag=0
    else:
        content = markdown.markdown(util.get_entry(title))
        flag=1
    return render(request, "encyclopedia/pages.html", {
        "name": content,
        "title":title,
        "flag":flag
    })

def search(request):
    if 'q' in request.POST:
        q = request.POST['q']
        entries = util.list_entries()
        if q in entries:
            return page(request, q)
        else:
            topics=[]
            for entry in entries:
                if q in entry:
                    topics.append(entry)
            return render(request, "encyclopedia/results.html", {
                "entries": topics
            })
    else:
        q=False
        return HttpResponse("Error in the page.")

def new(request):
    if request.method=="POST":
        title = request.POST['title']
        content = request.POST['content']
        entries = util.list_entries()
        if title in entries:
            return HttpResponse("<h1>Error!</h1><p>The page already exists.")
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("title", args=(title,)))
    else:
        return render(request, "encyclopedia/new.html")

def edit(request, title):
    content = util.get_entry(title)
    if request.method=="POST":
        info = request.POST['content']
        util.save_entry(title, info)
        return HttpResponseRedirect(reverse("title", args=(title,)))
    return render(request, "encyclopedia/edit.html", {
        "title":title,
        "content":content
    })

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return page(request, title)





