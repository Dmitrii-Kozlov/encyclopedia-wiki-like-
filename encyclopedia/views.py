from django.http import Http404
from django.shortcuts import render
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, name):
    page = markdown2.markdown( util.get_entry(name))
    if not page:
        raise Http404("Page does not exist")
    return render(request, "encyclopedia/page.html", {
        "title":name,
        "content": page
    })

