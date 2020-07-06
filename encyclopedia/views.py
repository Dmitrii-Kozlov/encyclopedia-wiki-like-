import random

from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
import markdown2
from django.urls import reverse
from django import forms
from . import util



def validate_name(name):
    if name.lower() in [x.lower() for x in util.list_entries()]:
        raise ValidationError(f'{name} is already exist!')
class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title", validators=[validate_name])
    text = forms.CharField(widget=forms.Textarea(attrs={"rows":15, "cols":20}))



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, name):
    for x in util.list_entries():
        if name.lower() == x.lower():
            name = x
    page = markdown2.markdown( util.get_entry(name))
    if not page:
        raise Http404("Page does not exist")
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
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("page", args=(title,)))
        else:
            return render(request, "encyclopedia/create_page.html", {
                "form": form
            })
    return render(request, "encyclopedia/create_page.html", {
        "form": NewTaskForm()
    })