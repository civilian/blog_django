from django.shortcuts import render, redirect
from posts.models import Post

def home_page(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts':  posts})
