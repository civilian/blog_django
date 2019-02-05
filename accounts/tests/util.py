from faker import Faker
import factory

from django.contrib.auth import get_user_model

def get_register_dict_from_user(user):
    data = {'username': user.username,
        'email': user.email,
        'password': user.password,
        'retype_password': user.password,
    }
    return data

def get_login_dict_from_user(user):
    """Returns a dictionary with the data needed to
    login a user but the password is 'password' because the object
    of a user saves the hashed password and not the actual password"""
    data = {'username': user.username,
        'password': 'password',
    }
    return data

def get_unsaved_user(*args, **kwargs):
    """Returns a user that has not been saved with the 
    password 'password' instead of a saved password that is long
    and comes with the salt"""
    user = UserFactory.build(*args, **kwargs)
    user.password = 'password'
    return user

class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = get_user_model()

    username = 'nato'
    email = 'nato@nato.com'
    password = factory.PostGenerationMethodCall('set_password', 'password')
