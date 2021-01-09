from django.shortcuts import render
import markdown2
from random import choice
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files import File
from . import util
from django import forms
from django.urls import reverse
from django.core.files.storage import default_storage
import os

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)

class SearchFormEdit(forms.Form):
    query = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': 'Search Wiki',
            'style': 'width:100%'}))

class CreateForm(forms.Form):
    title = forms.CharField(label="Add Title")
    body = forms.CharField(label="Add Body", widget=forms.Textarea(
        attrs={'rows': 1, 'cols': 10}))

class EditPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        'id': 'edit-entry-title'}))
    data = forms.CharField(label="", widget=forms.Textarea(attrs={
        'id': 'edit-entry'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    mark = markdown2.Markdown()
    page = util.get_entry(title)

    if page is None:
        return render(request, "encyclopedia/error.html", {

        })

    return render(request, "encyclopedia/entry.html", {
        "title": title.capitalize(),
        "content": mark.convert(util.get_entry(title)),
    })

def addpage(request):
     mark = markdown2.Markdown()
     if request.method == "POST":
        createform = CreateForm(request.POST)
        if createform.is_valid():
            title = createform.cleaned_data.get("title")
            body = createform.cleaned_data.get("body")
            present = False
            for entry in util.list_entries():
                if title == entry:
                    present = True
                    break
            if present:
                return render(request, "encyclopedia/titleerror.html")
            else:
                util.save_entry(title, body)
                form = SearchForm()
                mdcontent = util.get_entry(title)
                htmlcontent = mark.convert(mdcontent)
                return render(request, "encyclopedia/entry.html", {
                    "title": title, "content": htmlcontent, "form": form
                })
    # if request medthod is GET
     else:
        form = SearchForm()
        createform = CreateForm()
        return render(request, "encyclopedia/add.html", {"form": form, "createform": createform})


def edit(request, title):
    if request.method == "POST":
        entry = util.get_entry(title)
        edit_form = EditPageForm(initial={'title': title, 'data': entry})
        return render(request, "encyclopedia/edit.html", {
            "form": SearchFormEdit(),
            "editPageForm": edit_form,
            "entry": entry,
            "title": title
        })

def submitedit(request, title):
    mark = markdown2.Markdown()
    if request.method == "POST":
        edit_entry = EditPageForm(request.POST)
        if edit_entry.is_valid():
            content = edit_entry.cleaned_data["data"]
            title_edit = edit_entry.cleaned_data["title"]
            if title_edit != title:
                filename = f"entries/{title}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
            util.save_entry(title_edit, content)
            entry = util.get_entry(title_edit)
            msg_success = "Successfully updated!"
        return render(request, "encyclopedia/entry.html", {
            "title": title_edit,
            "entry": mark.convert(entry),
            "form": SearchFormEdit(),
            "msg_success": msg_success
        })


def randompage(request):
    return entry(request,choice( util.list_entries()))

def search(request):
     mark = markdown2.Markdown()
     if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get("query")
            present = False
            for entry in util.list_entries():
                if data == entry:
                    mdcontent = util.get_entry(data)
                    htmlcontent = mark.convert(mdcontent)
                    present = True
                    break
            if present:
                return render(request, "encyclopedia/entry.html", {"content": htmlcontent, "form": form, "title": data})
            else:
                lst = []
                for entry in util.list_entries():
                    if data in entry:
                        lst.append(entry)
                if len(lst) == 0:
                    return render(request, "encyclopedia/error.html")
                else:
                    return render(request, "encyclopedia/index.html", {
                        "entries": util.list_entries()
                    })
     else:
        form = SearchForm()
        content = "Search for some page in order to see the result"
        return render(request, "encyclopedia/error.html", {'form': form, "content": content})
