from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('signup', views.sign_up, name='signup'),
]
