import pytest
from django.core.management import call_command


@pytest.fixture(scope='session')
def test_initial_users(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'initial_users.json',)
        call_command('loaddata', 'users_data',)
