from datetime import datetime

import pytest
from django.test import Client
from django.urls import reverse

from my_api.models import Author, Book


@pytest.fixture
def test_author():
    return Author.objects.create(name="test_name", biography="test_biography")


@pytest.mark.django_db
def test_books_get_api(client: Client):
    author1 = Author.objects.create(name="test_name_1", biography="test_biography_1")
    author2 = Author.objects.create(name="test_name_2", biography="test_biography_2")
    book1 = Book.objects.create(
        title="test_title_1", author=author1, genre="fantasy", created_date="2007-10-10"
    )
    book2 = Book.objects.create(
        title="test_title_2", author=author2, genre="fantasy", created_date="2007-10-10"
    )

    response = client.get(reverse("books"))
    response_with_pk = client.get(reverse("one_book", kwargs={"book_id": book1.id}))

    assert response.status_code == 200
    assert response_with_pk.status_code == 200

    assert (
        response_with_pk.json()['books'][0]["id"] == book1.id
        and response_with_pk.json()['books'][0]["id"] != book2.id
    )
    assert response_with_pk.json()['books'][0]["title"] == book1.title
    assert response_with_pk.json()['books'][0]["author"] == book1.author.name
    assert response_with_pk.json()['books'][0]["genre"] == book1.genre
    assert response_with_pk.json()['books'][0]["created_date"] == book1.created_date


@pytest.mark.django_db
def test_books_post_api(client: Client, test_author):
    data = {
        'book': {
            'title': 'Test Title',
            'author': str(test_author.id),
            'genre': 'Test Genre',
            'created_date': '2007-10-10',
        }
    }

    response = client.post(
        reverse("books"), data=data, content_type='application/json'
    )

    assert response.status_code == 200

    created_book = Book.objects.get(id=response.json()['books'][0]["id"])

    assert created_book.title == data['book']["title"]
    assert created_book.genre == data['book']["genre"]
    assert str(created_book.created_date) == data['book']["created_date"]

    assert response.json()['books'][0]["title"] == data['book']["title"]
    assert response.json()['books'][0]["genre"] == data['book']["genre"]
    assert response.json()['books'][0]["created_date"] == data['book']["created_date"]


@pytest.mark.django_db
def test_books_update_api(client: Client, test_author):
    book = Book.objects.create(title="test_title_4", author=test_author, genre="fantasy", created_date="2007-10-10")

    data = {
        'book': {
            "title": "Test Title",
            "author": str(test_author.id),
            "genre": "Test Genre",
            "created_date": '2007-10-10',
        }
    }

    url = reverse("one_book", kwargs={"book_id": book.id})
    response = client.put(
        url, data=data, content_type="application/json"
    )

    assert response.status_code == 200

    date_format = "%Y-%m-%d"
    expected_created_date = datetime.strptime(
        data['book']["created_date"], date_format
    ).date()

    updated_book = Book.objects.get(id=book.id)

    assert updated_book.title == data['book']["title"]
    assert updated_book.genre == data['book']["genre"]
    assert updated_book.created_date == expected_created_date


@pytest.mark.django_db
def test_books_delete_api(client: Client, test_author):
    book_for_deleted = Book.objects.create(
        title="Test Title",
        author=test_author,
        genre="Test Genre",
        created_date='2007-10-10',
    )

    url = reverse("one_book", kwargs={"book_id": book_for_deleted.id})
    response = client.delete(url)

    assert response.status_code == 200
