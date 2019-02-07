from django.shortcuts import render
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import SignUpUserForm

def signup(request):
    """Creates a user if the data is correct"""
    if request.method == 'POST':
        form = SignUpUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'The user has been created')
            return redirect(reverse('home'))
        messages.error(request, 'The password is wrong or the user has already been created')
        return redirect(reverse('home'))


def login(request):
    """Logs in a user"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'The user has been logged in')
        return redirect(reverse('home'))


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'The user has been logged out')
        return redirect(reverse('home'))

