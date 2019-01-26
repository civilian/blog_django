from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import SignUpUserForm

def sign_up(request):
    """Creates a user if the data is correct"""
    if request.method == 'POST':
        form = SignUpUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'The user has been created')
            return redirect(reverse('home'))
        messages.error(request, 'The password is wrong or the user has already been created')
        return redirect(reverse('home'))

