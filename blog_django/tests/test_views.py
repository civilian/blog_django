from django.test import TestCase
from django.urls import reverse

class HomePageViewTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'blog_django/home.html')
