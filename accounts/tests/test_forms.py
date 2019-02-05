from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.forms import ( 
                SignUpUserForm, PASSWORD_DONT_MATCH, 
                USERNAME_ALREADY_IN_USER)
from accounts.tests import util
from accounts.tests.util import UserFactory

User = get_user_model()

class SignUpUserFormTest(TestCase):

    def test_form_renders_inputs_and_labels(self):
        form = SignUpUserForm()
        self.assertIn('class="form-control"', form.as_p())


    def test_no_errors_if_data_is_correct(self):
        user = util.get_unsaved_user()
        data = util.get_register_dict_from_user(user)
        form = SignUpUserForm(data=data)
        self.assertTrue(form.is_valid())
        

    def test_form_validation_blank_content(self):
        user = util.get_unsaved_user(username='')
        data = util.get_register_dict_from_user(user)
        form = SignUpUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'],['This field is required.'])


    def test_form_save(self):
        user = util.get_unsaved_user()
        data = util.get_register_dict_from_user(user)

        form = SignUpUserForm(data)
        form.is_valid()
        new_user = form.save()

        self.assertEqual(new_user, User.objects.first())


    def test_form_validation_username(self):
        """Creates a user and then creates that user again so that the
        Test can check the error or repeated username"""
        UserFactory()
        user = util.get_unsaved_user()
        data = util.get_register_dict_from_user(user)
        form = SignUpUserForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'],
            [USERNAME_ALREADY_IN_USER % user.username])


    def test_form_validation_retype_password(self):
        user = util.get_unsaved_user()
        data = util.get_register_dict_from_user(user)
        data['password'] = 'badpassword'

        form = SignUpUserForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['retype_password'],
            [PASSWORD_DONT_MATCH])
