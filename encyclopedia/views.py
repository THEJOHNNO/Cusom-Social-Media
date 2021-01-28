from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect
from . import util
from django.urls import reverse
import random
import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "allPages":"All Entries"
    })


def getContent(request, title):
    entryContent = util.get_entry(title)
    if entryContent:
        return render(request, "encyclopedia/entry.html", {
            "entryContent": markdown.markdown(entryContent),
            "allPages":f"{title}",
            "title":title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "allPages":"404 Not Found",
            "errorCode":HttpResponseNotFound(),
            "errorMessage":f"The requested page for '{title}' was not found."
        })

def wikiSearch(request):

    searchQuery = request.GET["q"]

    if util.get_entry(searchQuery):
        return HttpResponseRedirect(reverse('encyclopedia:getContent', kwargs={'title':searchQuery}))
    else:
        return render(request, "encyclopedia/index.html", {
            "entries":list(filter(lambda s: searchQuery.upper() in s.upper(), util.list_entries())),
            "allPages":"Search Results:"
        })


def newPage(request):
    return render(request, "encyclopedia/newEntry.html")

def newEntry(request):
    pageTitle = request.GET["pageTitle"]
    markdownContent = request.GET["markdownContent"]

    if pageTitle in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "allPages":"Error: Already Exists",
            "errorMessage":f"The requested page already exists."
        })
    else:
        util.save_entry(pageTitle, markdownContent)
        return HttpResponseRedirect(reverse('encyclopedia:getContent', kwargs={'title':pageTitle}))

def editPage(request, title):
    prePopulated = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "prePopulated":prePopulated,
        "title":title,
    })

def writeEdit(request, title):
    markdownContent = request.POST.get('markdownContent')
    util.save_entry(title, markdownContent)
    return HttpResponseRedirect(reverse('encyclopedia:getContent', kwargs={'title':title}))

def randomPage(request):
    return HttpResponseRedirect(reverse("encyclopedia:getContent", kwargs={
        "title": random.choice(util.list_entries())
    }))
