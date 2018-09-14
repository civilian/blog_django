import tempfile
import datetime
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from posts.models import Post

# def get_temporary_image():
#     size = (200, 200)
#     color = (255, 0, 0, 0)
#     image = Image.new("RGBA", size, color)
#     # temp_file = tempfile.NamedTemporaryFile()
#     temp_file = BytesIO(image.tobytes())
#     # image.save(temp_file, 'png')
#     temp_file.name = 'test.png'
#     temp_file.seek(0)
#     # image.save('new', 'png')
#
#     return temp_file

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
        publication_date = now.strftime("%Y-%m-%d")

    if expiring_date == None:
        a_week = datetime.timedelta(days=7)
        a_week_from_now = now + a_week
        expiring_date = a_week_from_now.strftime("%Y-%m-%d")

    if image == None:
        test_image = get_temporary_image()
        image = SimpleUploadedFile(name=test_image.name,
            content=open(test_image.name, 'rb').read(),
            content_type='image/png')

    post.title = title
    post.content = content
    post.image = image
    post.publication_date = publication_date
    post.expiring_date = expiring_date
    return post


def get_valid_post_object():
    return get_custom_post_object()
