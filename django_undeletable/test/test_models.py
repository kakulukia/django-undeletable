from django.db import models
from django.test import TestCase

from django_undeletable.models import NamedModel


class Author(NamedModel):
    pass


class Book(NamedModel):
    author = models.ForeignKey(Author, related_name='books',
                               related_query_name='author', on_delete=models.SET_NULL)
    co_authors = models.ManyToManyField(Author, related_name='featured_books',
                                        related_query_name='author')


class HideDeletedBooks(TestCase):
    def setup(self):
        visible_author = Author.data.create(name='visible')
        deleted_author = Author.data.create(name='deleted')

        visible_book = Book.data.create(
            name='visible book',
            author=visible_author
        )
        visible_book.co_authors.add(visible_author)
        visible_book.co_authors.add(deleted_author)

        deleted_book = Book.data.create(
            name='deleted book',
            author=visible_author
        )
        deleted_book.co_authors.add(visible_author)
        deleted_book.co_authors.add(deleted_author)

        deleted_author.delete()
        deleted_author.delete()

        self.visible_book = visible_book
        self.visible_author = visible_author
        self.deleted_book = deleted_book
        self.deleted_author = deleted_author

    def check_correct_visibility(self):

        self.assertCountEqual(Author.data.count(), 1)
        self.assertCountEqual(Book.data.count(), 1)

    def deleted_models_are_filtered_out_by_the_related_query_manager(self):
        pass


