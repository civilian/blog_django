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

def get_custom_post_object(title='New Post',
                            content='Awesome new blog post',
                            image=None,
                            publication_date=None,
                            expiring_date=None):
    post = Post()

    now = datetime.datetime.now()

    if publication_date == None:
        # publication_date = now.strftime("%Y-%m-%d")
        publication_date = now

    if expiring_date == None:
        a_week = datetime.timedelta(days=7)
        a_week_from_now = now + a_week
        # expiring_date = a_week_from_now.strftime("%Y-%m-%d")
        expiring_date = a_week_from_now

    if image == None:
        test_image = get_temporary_image()
        # image = InMemoryUploadedFile(test_image.name,
        #     open(test_image.name, 'rb').read())
        image = SimpleUploadedFile(name=test_image.name,
            content=open(test_image.name, 'rb').read(),
            content_type='image/png')

    post.title = title
    post.content = content
    post.image = image
    post.publication_date = publication_date
    post.expiring_date = expiring_date
    return post


def get_expiring_date(publication_date):
    a_week = datetime.timedelta(days=7)
    a_week_from_now = publication_date + a_week
    return a_week_from_now


def get_test_image():
    test_image = get_temporary_image()
    return SimpleUploadedFile(name=test_image.name,
        content=open(test_image.name, 'rb').read(),
        content_type='image/png')

def get_valid_post_object():
    return get_custom_post_object()


def get_dict_from_post(post):
    data = {'title': post.title,
        'content': post.content,
        'image': post.image,
        'publication_date': post.publication_date.strftime("%Y-%m-%d"),
        'expiring_date': post.expiring_date.strftime("%Y-%m-%d"),
    }
    return data

class PostFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Post
        django_get_or_create = ['title', 'content', 'image', 'publication_date',
                                'expiring_date']

    title = 'Title blog post'
    content ='Content for blog post'
    image = get_test_image()
    publication_date = datetime.datetime.now()
    expiring_date = get_expiring_date(publication_date)
