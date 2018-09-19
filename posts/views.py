from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from posts.forms import PostForm

def create(request):
    form = PostForm()
    return render(request, 'posts/create.html', {'form': form})


def store(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'The blog post has been created') 
            return redirect(reverse('posts:show'))
        return render(request, 'posts/create.html', {'form': form})


def show(request):
    return render(request, 'posts/show.html')
