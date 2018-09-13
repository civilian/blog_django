from django.urls import path, include

from blog_django import views as blog_views

urlpatterns = [
    path('', blog_views.home_page, name='home'),
    path('posts/', include('posts.urls')),
]
