import tempfile
import datetime

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
    

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_displays_only_non_expired_posts(self):
        PostFactory(title='Good post')

        expired_post = PostFactory.build(title='Expired post')
        expired_post.publication_date = datetime.date.today() - datetime.timedelta(1)
        expired_post.expiring_date = datetime.date.today() - datetime.timedelta(1)
        expired_post.save()

        response = self.client.get(reverse('home'))

        self.assertContains(response, 'Good post')
        self.assertNotContains(response, 'Expired post')


    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_displays_post_that_expire_today(self):
        today_expires_post = PostFactory.build(title='Today expires post')
        today_expires_post.publication_date = datetime.date.today()
        today_expires_post.expiring_date = datetime.date.today()
        today_expires_post.save()
        
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'Today expires post')
    

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_displays_only_publicated_posts(self):
        PostFactory(title='Publicated post')

        expired_post = PostFactory.build(title='Not publicated post')
        expired_post.publication_date = datetime.date.today() + datetime.timedelta(1)
        expired_post.save()

        response = self.client.get(reverse('home'))

        self.assertContains(response, 'Publicated post')
        self.assertNotContains(response, 'Not publicated post')
    
