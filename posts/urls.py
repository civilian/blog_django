from django.urls import path

from posts import views

app_name = 'posts'
urlpatterns = [
    path('create', views.create, name='create'),
    path('store', views.store, name='store'),
    # TODO: need the tests for show
    path('show', views.show, name='show'),
]
