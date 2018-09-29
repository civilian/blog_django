from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse

from posts.forms import PostForm
from posts.models import Post

def create(request):
    form = PostForm()
    return render(request, 'posts/create.html', {'form': form})


def store(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'The blog post has been created')
            return redirect(reverse('posts:show', kwargs={'post_id': post.id}))
        return render(request, 'posts/create.html', {'form': form})


def show(request,  post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/show.html', {'post': post})


def index(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})


def edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=post)
    return render(request, 'posts/edit.html', {'form': form})


def update(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'The blog post has been updated')
            return redirect(reverse('posts:show', kwargs={'post_id': post.id}))
        return render(request, 'posts/edit.html', {'form': form})


def delete(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        messages.success(request, 'The blog post has been succesfully deleted')
        return redirect(reverse('posts:index'))


def ajax_publication_date(request, post_id):
    if request.is_ajax():
        post = get_object_or_404(Post, id=post_id)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            data = {
                'message' : 'The publication date has been saved.'
            }
        else:
            publication_date_errors = form.errors.get('publication_date')
            if publication_date_errors == None:
                data = {
                    'message' : 'The publication date has not been saved.'
                }
            else:
                data = {
                    'message' : form.errors['publication_date'][0]
                }
        return JsonResponse(data)