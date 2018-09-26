import tempfile

from faker import Faker
from django.test import TestCase
from django.urls import reverse
from django.test import override_settings

from posts.tests.util import PostFactory
from posts.tests import util

class HomePageViewTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'blog_django/home.html')
    
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_displays_correct_posts(self):
        PostFactory(title='first post title')
        PostFactory(title='second post title')
        PostFactory.build(title='This post has not been saved')

        response = self.client.get(reverse('home'))

        self.assertContains(response, 'first post title')
        self.assertContains(response, 'second post title')
        self.assertNotContains(response, 'This post has not been saved')
    

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_displays_trimmed_content(self):
        fake = Faker()
        post = util.save_valid_post_object(content=fake.sentence(nb_words=100))

        response = self.client.get(reverse('home'))

        trimmed_content = post.content[:97] + '...'
        self.assertContains(response, trimmed_content)
