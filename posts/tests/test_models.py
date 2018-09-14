import tempfile
from django.test import TestCase, override_settings

from posts.tests import util
from posts.models import Post

class PostModelTest(TestCase):

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_can_save_valid_post_object(self):
        post = util.get_valid_post_object()
        post.full_clean() ## should not raise
        post.save()
