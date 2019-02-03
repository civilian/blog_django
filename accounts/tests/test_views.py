from pprint import pprint

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from accounts.tests.util import UserFactory
from accounts.tests import util

User = get_user_model()

class SingUpViewTest(TestCase):

    def assertUserIsSavedCorrectly(self, user, saved_user):
        self.assertEqual(user.username, saved_user.username)
        self.assertEqual(user.email, saved_user.email)


    def test_redirects_to_home_view(self):
        user = UserFactory.build()
        response = self.client.post(
            reverse('accounts:sign_up'),
            data=util.get_register_dict_from_user(user)
        )
        self.assertRedirects(response, reverse('home'))
    
    
    def test_succesfully_sign_up_user(self):
        user = UserFactory.build()
        self.client.post(
            reverse('accounts:sign_up'),
            data=util.get_register_dict_from_user(user)
        )
        self.assertEqual(1, User.objects.count())
        self.assertUserIsSavedCorrectly(user, User.objects.first())
    
    
    def test_retype_password_incorrect_fails_to_sign_up(self):
        """Test when the password is incorrectly retyped the user is not created"""
        user = UserFactory.build()
        user_dict = util.get_register_dict_from_user(user)
        user_dict['retype_password'] = 'badpassword'
        self.client.post(
            reverse('accounts:sign_up'),
            data= user_dict
        )
        self.assertEqual(0, User.objects.count())
    

    def test_cant_sign_up_two_user_with_the_same_username(self):
        UserFactory()
        user = UserFactory.build()
        self.client.post(
            reverse('accounts:sign_up'),
            data=util.get_register_dict_from_user(user)
        )
        self.assertEqual(1, User.objects.count())


# class LoginViewTest(TestCase):

#     def test_redirects_to_home_view(self):
#         user = UserFactory()
#         response = self.client.post(
#             reverse('accounts:sign_up'),
#             data=util.get_register_dict_from_user(user)
#         )
#         self.assertRedirects(response, reverse('home'))