import pytest
from django.urls import reverse
from django.test import Client

from my_api.models import Author


@pytest.mark.django_db
def test_authors_api_get(client: Client):
    author1 = Author.objects.create(name="test_name_1", biography="test_biography_1")
    author2 = Author.objects.create(name="test_name_2", biography="test_biography_2")

    response = client.get(reverse("authors"))
    response_id = client.get(
        reverse("one_author", kwargs={"author_id": author1.id})
    )
    response_post = client.post(reverse("authors"))
    response_delete = client.delete(reverse("one_author", kwargs={"author_id": author1.id}))

    assert response.status_code == 200
    assert response_id.status_code == 200
    assert response_post.status_code == 405
    assert response_delete.status_code == 405

    assert (
        response_id.json()['authors'][0]["id"] == author1.id
        and response_id.json()['authors'][0]["id"] != author2.id
    )
    assert response_id.json()['authors'][0]['name'] == author1.name
    assert response_id.json()['authors'][0]["biography"] == author1.biography
