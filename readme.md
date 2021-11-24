

# Wiki


## Inline JS Delete button with CSFR

This will send a DELETE request with the required CSRF token.

```html
<!-- CSFR Used by CSRF oneliner -->
{% csrf_token %}
<!-- Nice oneliner CSRF Hack -->
<button type="button" class="btn btn-danger" 
    onclick="fetch('{% url 'view' name %}', {method: 'delete', headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value } }).then(() => {window.location = '{% url 'index' %}'})"
    >DELETE this post</button>
```

The code to treat this HTTP request can simply check the request method.

```python
# views.py
def view_post(request, name):
    if request.method == 'DELETE':
        util.delete_entry(name)
        messages.warning(request, f"Removed post \"{name}\"")
        return HttpResponse()
    # Rest of this function was removed.
```

The content of _urlpatterns_ in `urls.py`.

```py
urlpatterns = [
    # Other paths have been removed
    path('<str:name>', views.view_post, name="view"),
]
```

### Javascript or no Javascript, that is the question.

HTML forms have a crucial limitation, they can only send GET and POST requests.

I am not keen on polluting the URL with the content of my form fields.
This means that for most form submits I favor POST requests.

One exception being the search functionality.
Allowing search to work through a GET request and having the parameters
in the url `?q=searchterm` allows people to bookmark a specific search.

Using POST requests for everything means that a choice needs to be made.

Either you create a URL endpoint for the typical CRUD, create read update
operations that you want to take.

For example.

| URL              | GET Method                           | POST Method                  |
|------------------|--------------------------------------|------------------------------|
| `/new`           | Show the form to create a new post   | Create post (title, content) |
| `/edit/<name>`   | Show the form to edit a post         | Update post (title, content) |
| `/delete/<name>` | (optional) show a confirmation page  | Delete post (title)          |
| `/view/<name>`   | Shows the post                       | _Not used_                   |

An alternative way of going about this is using hidden fields to reduce the amount
of url endpoints that you need to create.

You could use the same url endpoint for creating a _new_ post and _editing_ an existing one by 
having a hidden field that differentiates between the two.

This could be a hidden checkbox called **edit** for example.

It is possible to take this aproach further and encoding all the possible actions
into a specific field, only needing one actual endpoint.

Here is an example of how you could use a hidden _action_ field 
in combination with only one url endpoint to deal with CRUD operations.

- /post
  - GET `/post` request display the post.
    - This page contains links to `/post?new=true` and `/post?edit=true` and a form with the hidden action = 'delete' to allow deleting the item.
  - GET `/post?new=true` display form to create a new post(hidden action field = `create`)
  - GET `/post?edit=true` display the edit form (hidden action field = `update`)
  - POST request to `/post`
    - when `action == 'create'`, the other paremeters are for creating a new post
    - when `action == 'update'`, the other parameters are for editing an existing post
    - when `action == 'delete'`, the other paremeters are for deleting an existing post

I have previously used such an approach when I really wanted to avoid
client-side javascript.

It does result in more server-side code that comes close to duplicate code.
Below is an extract of some Flask code I used for another project.

```py
if request.method == 'POST':
    action = request.form["action"]
    
    if action == 'create':
        # Read out the form fields
        # Validate their values
        # Create the item
    elif action == 'update':
        # Read out the form fields
        # Validate their values
        # Update the item
    elif action == 'delete':
        # Read out the form field, (usually only the item ID or something)
        # that uniquely identifies it.
        # Delete the item
```

Time to come around to the actual reason for this post.

HTTP has request methods, also called [verbs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods).
These request method each have an intended purpose.

- GET representation of the resource
- POST create of a resource
- PUT update of a resource
- DELETE delete a resource

As said before, HTML forms only support GET and POST.
With Javascript however, you can use whatever HTTP verbs you want.

```js
fetch('http://url/endpoint', { method: 'delete', headers: {}, body: {} })
```

This is an illustrative piece of code, to be able to do something we need a few more components.

1) An event listener to trigger this event.
2) A way to send the data. Often done by either putting JSON in the body or www-urlencoded values.
3) Add the **CSRF token** value. This can be one of the ww-urlencoded fields or a HTTP header.
4) Navigation towards another page or a page reload.

And those are the bare minimum, more eloborate setups sometimes include things like progress animations or at the very least disabling the button that triggered the event to prevent multiple 
HTTP requests to be launched.

My one-liner fits these requirements, be it the bare minimum.

First the event listener is a dirty `onclick=` attribute on the button element.

```html
<button type="button" class="btn btn-danger" 
    onclick="/* one-line JS code */"
    >DELETE this post</button>
```

Because this is a delete request, and not an update request. 
The only information that is required is something to uniquely identify 
the post. In this case the name is sufficient.
So the data is actually put into the URL.

```py
{% url 'view' name %} # results in http://localhost/posts/My%20Title
```

The `My%20Title` in the URL is enough information to know which post
to delete.

The next challenge is sending Django the CSRF token.
It is possible to disable the need for a CSRF token but that is not
recommended.

One way to provide the CSRF token is by putting it in the `X-CSRFToken` 
header. Adding something to a header is easy with `fetch()`.

```js
fetch(url, { headers: headers: { 'X-CSRFToken': '...' } })
```

Now we need a way to retrieve a CSRF token. There are ways to read out
the CSRF token value through cookies.
In this case however I prefered to read it from the hidden field that
is created by `{% csrf_token %}`. Inside the Django template
 `{% csrf_token %}` gets transformed to `<input type="hidden" name="csrfmiddlewaretoken" value="LTnlEXkhcPCloHd1f6eM2rbJ1gNh7KCGX38L9epMjejGqldSegyzlLlFLhlxj9M4">`

 To grab this HTML element we can use the `document.querySelector` function.

 ```js
document.querySelector('[name=csrfmiddlewaretoken]')
 ```

 We grab the element that has a _name_ attribute that is equal to **csrfmiddlewaretoken**.
From that element we retrieve the **value**.

```js
document.querySelector('[name=csrfmiddlewaretoken]').value 
```

Lastly we will want to do something once our DELETE request has occured.
We put `.then()` after `fetch()`. `then` takes a function as argument.
That is why I wrap my code with `() => { /* code */ }`.

```js
() => {window.location = '{% url 'index' %}'}
/* ECMA Script 5 version */
function() { window.location = '{% url 'index' %}' }
```

Navigating to another page in Javascript is done through setting the `window.location` value to a URL.

#### conclusion

Using Javascript in the front-end to trigger your CRUD operations,
 your back-end code will be able to check the request method and 
decide based on that what todo next.

```py
if request.method == 'DELETE':
    # code to delete the item
    # then redirect somehwere
elif request.method == 'PUT':
    # code to update the item
elif request.method == 'POST:
    # code to create the item

# Show the item
return render(request, 'show_item.html'
```

