import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from cartoview.log_handler import get_logger

logger = get_logger(__name__)


@pytest.mark.django_db
def test_api_smoke(client, test_initial_users):
    url = reverse('api:api-root')
    response = client.get(url)
    assert response.status_code == 200
    urls = response.json()
    auth_required = [urls.pop('simple_auth'), urls.pop('token_auth')]
    for url in urls.values():
        response = client.get(url)
        assert response.status_code == 200
    admin_user = get_user_model().objects.filter(is_superuser=True).first()
    client.force_login(admin_user)
    for url in auth_required:
        response = client.get(url)
        assert response.status_code == 200
