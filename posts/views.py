
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
    if not name in util.list_entries():
        return HttpResponseNotFound("Could not find post")

    post_content = util.get_entry(name)

    # Convert the markdown to HMTL
    html_content = markdown.markdown(post_content)

    return render(request, "post.html.j2", {
        'name': name, 
        'content': html_content
    })

def edit_post(request, name):
    if not name in util.list_entries():
        # Post doesn't exist, do we redirect?
        return HttpResponseNotFound("Could not find post")
    
    if request.method == 'POST':
        edit_form = forms.EditPost(request.POST)
        if edit_form.is_valid():
            content = edit_form.cleaned_data['content']
            util.save_entry(name, content)
            messages.info(request, "Saved changes")
        else:
            messages.error(request, "Failed to save changes (invalid form)")
    else:
        post_content = util.get_entry(name)
        edit_form = forms.EditPost(
            {'title': name, 'content': post_content})    

    return render(request, "edit_post.html.j2", {
        'name': name, 
        'edit_form': edit_form,
    })

def search_posts(request):
    results = []

    if 'q' in request.GET:
        query = request.GET['q']
        query_upper = query.upper()
        for title in util.list_entries():
            content = util.get_entry(title)
            if query_upper in content.upper() or query_upper in title.upper():
                results.append({'title': title, 'content': content})

    return render(request, "search_results.html.j2", {'results': results, 'query': query})

def delete_post(request, name):
    """
    Confirmation page to delete a post.
    """
    if request.method == 'POST':
        delete_form = forms.DeletePost(request.POST)
        if delete_form.is_valid():
            util.delete_entry(name)
            messages.info(request, "Deleted post")
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, "Failed to delete post (invalid form)")
    
    delete_form = forms.DeletePost({'title': name})
    return render(request, "delete_post.html.j2", {'name': name, 'delete_form': delete_form})
