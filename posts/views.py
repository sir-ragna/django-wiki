
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render

import markdown
from . import util
from . import forms

def new_post(request):
    post_form = forms.Post()
    return render(request, 'new_post.html.j2', { 
        'post_form': post_form
    })

def overview_posts(request):
    posts = util.list_entries()
    return render(request, 'posts.html.j2', {
        'posts': posts
    })

def view_post(request, post_name):
    if not post_name in util.list_entries():
        return HttpResponseNotFound("Could not find post")

    post_content = util.get_entry(post_name)

    # Convert the markdown to HMTL
    html_content = markdown.markdown(post_content)

    return render(request, "post.html.j2", {
        'name': post_name, 
        'content': html_content
    })

def delete_posts():
    pass

def edit_post():
    pass


