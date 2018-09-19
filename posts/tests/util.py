import tempfile
import datetime

import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from posts.models import Post

def get_temporary_image():
    temp_file = tempfile.NamedTemporaryFile(suffix='.png')

    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    temp_file.seek(0)

    return temp_file


def get_expiring_date(publication_date):
    a_week = datetime.timedelta(days=7)
    a_week_from_publication_date = publication_date + a_week
    return a_week_from_publication_date


def get_test_image():
    test_image = get_temporary_image()
    return SimpleUploadedFile(name=test_image.name,
        content=open(test_image.name, 'rb').read(),
        content_type='image/png')

def get_valid_post_object():
    post = PostFactory.build()
    post.image = get_test_image()
    return post


def get_dict_from_post(post):
    data = {'title': post.title,
        'content': post.content,
        'image': post.image,
        'publication_date': post.publication_date.strftime("%Y-%m-%d"),
        'expiring_date': post.expiring_date.strftime("%Y-%m-%d"),
    }
    return data

def get_date_with_time_delay(time_delay):
    date_with_time_delay = datetime.date.today() + datetime.timedelta(days=time_delay)
    return date_with_time_delay.strftime('%Y-%m-%d')

class PostFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Post
        django_get_or_create = ['title', 'content', 'image', 'publication_date',
                                'expiring_date']

    title = 'Title blog post'
    content ='Content for blog post'
    image = get_test_image()
    publication_date = datetime.date.today()
    expiring_date = get_expiring_date(publication_date)
