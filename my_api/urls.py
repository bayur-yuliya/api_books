from django.urls import path

from my_api import views

urlpatterns = [
    path('books/', views.create_book, name='books'),
    path('authors/', views.authors, name='authors')
]