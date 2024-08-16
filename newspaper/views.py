from django.shortcuts import render

# Create your views here.
from newspaper.models import Post

from django.views.generic import ListView


class HomeView(ListView):
    model=Post
    template_name="aznews/home.html"
    context_object_name="posts"
    