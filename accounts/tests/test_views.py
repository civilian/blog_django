from pprint import pprint

from django.test import TestCase
from django.urls import reverse

from accounts.tests.util import UserFactory
from accounts.tests import util

class RegisterUserViewTest(TestCase):

    def test_redirects_to_home_view(self):
        user = UserFactory.build()
        response = self.client.post(
            reverse('accounts:register'),
            data= util.get_dict_from_user(user)
        )
        self.assertRedirects(response, reverse('home'))
    
    # test_succesfully_logged_in_user