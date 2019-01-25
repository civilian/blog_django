from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        retype_password = request.POST.get('retype_password', '')
        # if form.is_valid():
        #     post = form.save()
        #     messages.success(request, 'The blog post has been created')
        #     return redirect(reverse('posts:show', kwargs={'post_id': post.id}))
        return redirect(reverse('home'))

