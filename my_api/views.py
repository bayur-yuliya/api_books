import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse

from my_api.models import Author, Book


def create_book(request):
    if request.method == "GET":
        books = Book.objects.all()

        title = request.GET.get("title")
        author = request.GET.get("author")
        genre = request.GET.get("genre")

        try:
            if title:
                books = Book.objects.filter(title=title)
            elif author:
                books = Book.objects.filter(author=Author.objects.get(name=author))
            elif genre:
                books = Book.objects.filter(genre=genre)

            if books.exists():
                result = JsonResponse({'books': [
                    {'id': b.id, 'title': b.title, 'author': b.author.name, 'genre': b.genre, 'created_date': b.created_date} for
                    b in books]}, status=200)
            # else:
            #     return JsonResponse({'massage': 'Books with this name not found'}, status=404)
        except Book.DoesNotExist:
            return JsonResponse({'massage': 'Books not found'}, status=404)
        except TypeError:
            result = JsonResponse({'books': [
                {'id': books.id, 'title': books.title, 'author': books.author.name, 'genre': books.genre, 'created_date': books.created_date}]}, status=200)
        return JsonResponse({'books': [
                    {'id': b.id, 'title': b.title, 'author': b.author.name, 'genre': b.genre, 'created_date': b.created_date} for
                    b in books]}, status=200)

    elif request.method == "POST":
        try:
            book = json.loads(request.body).get('book')
        except json.JSONDecodeError:
            return JsonResponse({'massage': 'Request body must by JSON'}, status=400)

        title = book['title']
        author = book['author']
        genre = book['genre']
        created_date = book['created_date']

        try:
            if len(title.strip()) > 0 and len(author.strip()) > 0 and len(genre.strip()) > 0:
                pass
            else:
                return JsonResponse({'massage': 'Title, author, genre is required'}, status=400)
        except TypeError:
            return JsonResponse({'massage': 'Title, author, genre must be string'}, status=400)

        author_created, created = Author.objects.get_or_create(name=author)

        try:
            books, created = Book.objects.get_or_create(title=title, author=author_created, genre=genre,
                                                        created_date=created_date)
            if created is False:
                return JsonResponse({'massage': 'Book was created early'}, status=400)
        except ValidationError:
            return JsonResponse({'massage': 'Created date is required'}, status=400)

        try:
            result = JsonResponse({'books': [
                {'id': b.id, 'title': b.title, 'author': b.author.name, 'genre': b.genre, 'created_date': b.created_date} for
                b in books]}, status=200)
        except TypeError:
            result = JsonResponse({'books': [
                {'id': books.id, 'title': books.title, 'author': books.author.name, 'genre': books.genre, 'created_date': books.created_date}]}, status=200)
        return result

    else:
        return JsonResponse({'massage': 'Incorrect method'}, status=405)


def one_book(request, book_id):
    if request.method == "GET":
        try:

            book = Book.objects.get(id=book_id)
            return JsonResponse({'books': [
                    {'id': book.id, 'title': book.title, 'author': book.author.name, 'genre': book.genre, 'created_date': book.created_date}]}, status=200)
        except Book.DoesNotExist:
            return JsonResponse({'massage': 'Book not found'}, status=404)

    elif request.method == "PUT":
        try:
            book = json.loads(request.body).get('book')
        except json.JSONDecodeError:
            return JsonResponse({'massage': 'Request body must by JSON'}, status=400)

        title = book['title']
        author = book['author']
        genre = book['genre']
        created_date = book['created_date']

        book = Book.objects.get(id=book_id)

        try:

            if title and len(title.strip()) > 0:
                book.title = title
                book.save()
            elif len(title.strip()) == 0:
                return JsonResponse({'massage': 'Title, author, genre must be string'}, status=400)

            if author and len(author.strip()) > 0:
                author_created, created = Author.objects.get_or_create(name=author)
                book.author = author_created
                book.save()
            elif len(author.strip()) == 0:
                return JsonResponse({'massage': 'Title, author, genre must be string'}, status=400)

            if genre and len(genre.strip()) > 0:
                book.genre = genre
                book.save()
            elif len(genre.strip()) == 0:
                return JsonResponse({'massage': 'Title, author, genre must be string'}, status=400)

            if created_date:
                book.created_date = created_date
                book.save()

        except ValidationError:
            return JsonResponse({'massage': 'Created date must be date'}, status=400)
        except AttributeError:
            return JsonResponse({'massage': 'Title, author, genre must be string'}, status=400)

        return JsonResponse({'books': [
                    {'id': book.id, 'title': book.title, 'author': book.author.name, 'genre': book.genre, 'created_date': book.created_date}]}, status=200)

    elif request.method == "DELETE":
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            return JsonResponse({'massage': 'Book is delete'}, status=200)
        except Book.DoesNotExist:
            return JsonResponse({'massage': 'Book not found'}, status=404)

    else:
        return JsonResponse({'massage': 'Incorrect method'}, status=405)


def authors(request):
    if request.method == "GET":
        name = request.GET.get("name")
        if name:
            try:
                authors = Author.objects.filter(name=name)
                if authors.exists():
                    return JsonResponse({'authors': [{'id': a.id, 'name': a.name, 'biography': a.biography} for a in authors]}, status=200)
                else:
                    return JsonResponse({'massage': 'Authors with this name not found'}, status=404)
            except Author.DoesNotExist:
                return JsonResponse({'massage': 'Authors not found'}, status=404)

        try:
            authors = Author.objects.all()
            return JsonResponse({'authors': [{'id': a.id, 'name': a.name, 'biography': a.biography} for a in authors]}, status=200)
        except Author.DoesNotExist:
            return JsonResponse({'massage': 'Authors not found'}, status=404)

    else:
        return JsonResponse({'massage': 'Incorrect method'}, status=405)


def one_author(request, author_id):
    if request.method == "GET":
        try:
            authors = Author.objects.get(id=author_id)
            return JsonResponse({'authors': [{'id': authors.id, 'name': authors.name, 'biography': authors.biography}]}, status=200)
        except Author.DoesNotExist:
            return JsonResponse({'massage': 'Author not found'}, status=404)
    else:
        return JsonResponse({'massage': 'Incorrect method'}, status=405)
