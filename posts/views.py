from django.shortcuts import render

from posts.forms import PostForm

def create(request):
    form = PostForm()
    return render(request, 'posts/create.html', {'form': form})
