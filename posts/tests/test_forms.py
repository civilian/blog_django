from django.test import TestCase

from posts.forms import PostForm

class PostFormTest(TestCase):

    def test_form_renders_inputs_and_labels(self):
        form = PostForm()
        self.assertIn('class="form-control"', form.as_p())
