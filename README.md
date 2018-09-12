# Blog Django

This is a simple blog developed in Django.

## Installation

Linux

```sh
$ pip install --upgrade virtualenv
$ virtualenv -p /usr/bin/python3.6 venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

To execute
```sh
$ source venv/bin/activate
$ python manage.py runserver
```

## Development setup

To install the dependencies for testing

```sh
$ pip install -r test-requirements.txt
```

To execute the tests

```sh
$ source venv/bin/activate
$ python manage.py test
```

## TODO
1. Put the .env.example file.
2. The instructions to use the Vagrantfile and the ansible.
3. Functional tests can be executed in the vagrant machine.
4. Decide what to do with the role provision-project-foundation
