
from django.http import HttpResponse

def mainpage(request):
    return HttpResponse("""<a href="/posts">Go to posts</a>""")
