from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from blog_django import views as blog_views

urlpatterns = [
    path('', blog_views.home_page, name='home'),
    path('posts/', include('posts.urls')),
]

# TODO: Test in staging what happens to the url
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
