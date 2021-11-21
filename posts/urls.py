
from django.urls import path

from . import views

urlpatterns = [
    #path('new/', posts.new_post),
    path('', views.overview_posts, name="index"),
    path('<str:post_name>', views.view_post, name="view"),
]

