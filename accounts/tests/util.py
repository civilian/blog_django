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

class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = get_user_model()

    username = 'nato'
    email = 'nato@nato.com'
    password = factory.Faker('password')
