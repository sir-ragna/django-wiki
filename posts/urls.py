
from django.urls import path

from . import views

urlpatterns = [
    #path('new/', posts.new_post),
    path('', views.overview_posts, name="index"),
    path('new', views.new_post, name="new post"),
    path('<str:name>', views.view_post, name="view"),
]

