from pprint import pprint

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import auth

from accounts.tests import util
from accounts.tests.util import UserFactory

User = get_user_model()

class SingUpViewTest(TestCase):

    def assertUserIsSavedCorrectly(self, user, saved_user):
        self.assertEqual(user.username, saved_user.username)
        self.assertEqual(user.email, saved_user.email)


    def test_redirects_to_home_view(self):
        user = util.get_unsaved_user()
        response = self.client.post(
            reverse('accounts:signup'),
            data=util.get_register_dict_from_user(user)
        )
        self.assertRedirects(response, reverse('home'))
    
    
    def test_succesfully_signup_user(self):
        user = util.get_unsaved_user()
        self.client.post(
            reverse('accounts:signup'),
            data=util.get_register_dict_from_user(user)
        )
        self.assertEqual(1, User.objects.count())
        self.assertUserIsSavedCorrectly(user, User.objects.first())
    
    
    def test_retype_password_incorrectly_fails_to_sign_up(self):
        """Test when the password is incorrectly retyped the user is not created"""
        user = util.get_unsaved_user()
        user_dict = util.get_register_dict_from_user(user)
        user_dict['retype_password'] = 'badpassword'
        self.client.post(
            reverse('accounts:signup'),
            data=user_dict
        )
        self.assertEqual(0, User.objects.count())
    

    def test_cant_sign_up_two_users_with_the_same_username(self):
        UserFactory()
        user = UserFactory.build()
        self.client.post(
            reverse('accounts:signup'),
            data=util.get_register_dict_from_user(user)
        )
        self.assertEqual(1, User.objects.count())


class LoginViewTest(TestCase):

    def test_redirects_to_home_view(self):
        user = util.get_unsaved_user()
        response = self.client.post(
            reverse('accounts:login'),
            data=util.get_login_dict_from_user(user),
        )
        self.assertRedirects(response, reverse('home'))
    

    def test_logs_in_correct_user(self):
        user = UserFactory()
        self.client.post(
            reverse('accounts:login'),
            data=util.get_login_dict_from_user(user),
        )
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
    

    def test_cant_log_incorrect_password_for_user(self):
        user = UserFactory()
        data = util.get_login_dict_from_user(user)
        data['password'] = 'badpassword'
        self.client.post(
            reverse('accounts:login'),
            data=data,
        )
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
    
    
    def test_cant_log_incorrect_user(self):
        UserFactory()
        user = UserFactory.build(username='newuseer')
        self.client.post(
            reverse('accounts:login'),
            data=util.get_login_dict_from_user(user),
        )
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        
