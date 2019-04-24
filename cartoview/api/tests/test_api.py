import pytest
from django.urls import reverse
from cartoview.log_handler import get_logger
logger = get_logger(__name__)


@pytest.mark.django_db
def test_api_smoke(client):
    url = reverse('api:api-root')
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    for url in data.values():
        response = client.get(url)
        assert response.status_code == 200
