from faker import Faker
import factory

from django.contrib.auth import get_user_model

def get_dict_from_user(user):
    data = {'username': user.title,
        'email': user.content,
        'password': user.image,
    }
    return data

class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = get_user_model()

    username = 'nato'
    email = 'nato@nato.com'
    password = factory.Faker('password')
