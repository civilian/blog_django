from django.urls import path

from posts import views

app_name = 'posts'
urlpatterns = [
    path('create', views.create, name='create'),
    path('store', views.store, name='store'),
    path('show/<int:post_id>/', views.show, name='show'),
    path('index/', views.index, name='index'),
    path('edit/<int:post_id>/', views.edit, name='edit'),
    path('update/<int:post_id>/', views.update, name='update'),
    path('delete/<int:post_id>/', views.delete, name='delete'),
    path('ajax_publication_date/<int:post_id>/', views.ajax_publication_date, name='ajax_publication_date'),
]
