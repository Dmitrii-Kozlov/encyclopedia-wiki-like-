import random

from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
import markdown2
from django.urls import reverse
from django import forms
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, name):
    if request.method == 'POST':
        content = util.get_entry(name)
        return render(request, "encyclopedia/edit_page.html", {
            "title": name,
            "content": content
        })
    for x in util.list_entries():
        if name.lower() == x.lower():
            name = x
    if not util.get_entry(name):
        raise Http404("Page does not exist")
    page = markdown2.markdown( util.get_entry(name))
    return render(request, "encyclopedia/page.html", {
        "title":name,
        "content": page
    })

def found_page(request):
    if request.method == 'POST':
        title = request.POST.get('q')
        if title.lower() in [x.lower() for x in util.list_entries()]:
            return HttpResponseRedirect(reverse("page", args=(title,)))
        else:
            pages = [page for page in util.list_entries() if title.lower() in page.lower()]
            return render(request, "encyclopedia/found_pages.html", {
                "entries": pages
            })
    else:
        title = random.choice(util.list_entries())
        return HttpResponseRedirect(reverse("page", args=(title,)))

def create_page(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        text = request.POST.get("text")
        if title.lower() not in [x.lower() for x in util.list_entries()]:
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("page", args=(title,)))
        else:
            return render(request, "encyclopedia/create_page.html", {
                'error': f'{title} page is already exist!',
                'title': title,
                'text':text
            })
    else:
        return render(request, "encyclopedia/create_page.html")

def save_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        util.save_entry(title,text)
        return HttpResponseRedirect(reverse("page", args=(title,)))