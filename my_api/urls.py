from django.urls import path

from my_api import views

urlpatterns = [
    path('books/', views.create_book, name='books'),
    path('books/<int:book_id>', views.one_book, name='one_book'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:author_id>', views.one_author, name='one_author'),
]