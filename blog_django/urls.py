from django.urls import path

from blog_django import views as blog_views

urlpatterns = [
    path('', blog_views.home_page, name='home'),
]