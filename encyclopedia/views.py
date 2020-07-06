from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
import markdown2
from django.urls import reverse

from . import util


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
