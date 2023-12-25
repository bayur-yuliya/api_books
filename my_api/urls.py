from django.urls import path

from my_api.views import BooksView, OneAuthorView, OneBookView, AuthorsView

urlpatterns = [
    path('books/', BooksView.as_view(), name='books'),
    path('books/<int:book_id>', OneBookView.as_view(), name='one_book'),
    path('authors/', AuthorsView.as_view(), name='authors'),
    path('authors/<int:author_id>', OneAuthorView.as_view(), name='one_author'),
]