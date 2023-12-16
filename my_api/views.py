import json
from django.http import JsonResponse

from my_api.models import Author, Book


def create_book(request):
    if request.method == "GET":
        return JsonResponse({'massage': 'Hello world'})
    if request.method == "POST":
        return JsonResponse({'massage': 'Hello world'})
    else:
        return JsonResponse({'massage': 'Incorrect method'}, status=405)


def authors(request):
    if request.method == "GET":
        authors = Author.objects.all()
        return JsonResponse({'authors': [{'id': a.id, 'name': a.name} for a in authors]}, status=200)
    if request.method == "POST":
        try:
            name = json.loads(request.body).get('name')
        except json.JSONDecodeError:
            return JsonResponse({'massage': 'Request body must by JSON'}, status=400)
        if not name:
            return JsonResponse({'massage': 'Name is required'}, status=400)
        author = Author.objects.create(name=name)
        return JsonResponse({'name': author.name, 'id': author.id}, status=201)
    else:
        return JsonResponse({'massage': 'Incorrect method'}, status=405)
