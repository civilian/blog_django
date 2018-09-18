import tempfile

from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.forms import PostForm
from posts.tests import util
from posts.tests.util import PostFactory
from posts.models import Post

class PostFormTest(TestCase):

    def test_form_renders_inputs_and_labels(self):
        form = PostForm()
        self.assertIn('class="form-control"', form.as_p())


    def test_no_errors_if_data_is_correct(self):
        post = util.get_valid_post_object()
        data = util.get_dict_from_post(post)
        form = PostForm(data=data)
        self.assertTrue(form.is_valid())


    def test_errors_with_incorrect_data(self):
        post = PostFactory.build(content='')
        data = util.get_dict_from_post(post)
        form = PostForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['content'],['This field is required.'])


    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_form_save(self):
        post = util.get_valid_post_object()
        data = util.get_dict_from_post(post)

        file_dict = {'image': post.image}
        form = PostForm(data, file_dict)
        new_post = form.save()

        self.assertEqual(new_post, Post.objects.first())


    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_form_saves_image(self):
        post = util.get_valid_post_object()
        data = util.get_dict_from_post(post)

        file_dict = {'image': post.image}
        form = PostForm(data, file_dict)
        new_post = form.save()

        self.assertEqual(post.image, Post.objects.first().image)
