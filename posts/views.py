
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib import messages

import markdown
from . import util
from . import forms

def new_post(request):
    if request.method == 'POST':
        post_form = forms.Post(request.POST)
        if post_form.is_valid():
            # We have a valid new post form
            title = post_form.cleaned_data['title']
            content = post_form.cleaned_data['content']

            # Check if the post doesn't already exist (to prevent overwritting)
            if not title in util.list_entries():
                util.save_entry(title, content)
                messages.info(request, "Post saved")
                return HttpResponseRedirect(reverse('view', kwargs={'name': title}))
            else:
                messages.error(request, "Error: Failed to save post (already exists)")    
        else: # not is_valid()
            messages.error(request, "Error: Failed to save post (invalid form)")
    else: # not a POST
        post_form = forms.Post()
    
    return render(request, 'new_post.html.j2', { 
        'post_form': post_form
    })

def overview_posts(request):
    posts = util.list_entries()
    return render(request, 'posts.html.j2', {
        'posts': posts
    })

def view_post(request, name):
    if request.method == 'DELETE':
        util.delete_entry(name)
        messages.warning(request, f"Removed post \"{name}\"")
        return HttpResponse()

    if not name in util.list_entries():
        return HttpResponseNotFound("Could not find post")

    post_content = util.get_entry(name)

    # Convert the markdown to HMTL
    html_content = markdown.markdown(post_content)

    return render(request, "post.html.j2", {
        'name': name, 
        'content': html_content
    })

def delete_posts():
    pass

def edit_post():
    pass


