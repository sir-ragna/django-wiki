
from django.http import HttpResponse
from django.shortcuts import render

from . import util

def new_post():
    pass

def overview_posts(request):
    posts = util.list_entries()
    return render(request, 'posts.html.j2', {'posts': posts})

def delete_posts():
    pass

def edit_post():
    pass

def view_post():
    pass

