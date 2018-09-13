from django.test import TestCase
from django.urls import reverse

from posts.forms import PostForm

class CreatePostTest(TestCase):

    def test_uses_create_post_template(self):
        response = self.client.get(reverse('create_post'))
        self.assertTemplateUsed(response, 'posts/create.html')


    def test_create_post_page_uses_post_form(self):
        response = self.client.get(reverse('create_post'))
        self.assertIsInstance(response.context['form'], PostForm)
