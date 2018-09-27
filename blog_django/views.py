import datetime

from django.shortcuts import render, redirect
from posts.models import Post

def home_page(request):
    today = datetime.date.today()
    posts = Post.objects.filter(expiring_date__gte=today)
    return render(request, 'blog_django/home.html', {'posts':  posts})
