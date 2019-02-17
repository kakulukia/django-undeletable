#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-undeletable
------------

Tests for `django-undeletable` models module.
"""
from django.conf import settings
from django.core import mail
from django.test import TestCase, override_settings

from test_app.models import Author, Book, TestUser, CoverBook


class TestDeletion(TestCase):
    def test_model_deletion(self):
        author = Author.data.create(name="John")
        self.assertEqual(Author.data.count(), 1)
        self.assertEqual(Author.data.deleted().count(), 0)

        author.delete()
        self.assertEqual(Author.data.count(), 0)
        self.assertEqual(Author.data.deleted().count(), 1)

        Author.data.deleted().undelete()
        self.assertEqual(Author.data.count(), 1)
        self.assertEqual(Author.data.deleted().count(), 0)


class GeneralTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        visible_author = Author.data.create(name="visible")
        deleted_author = Author.data.create(name="deleted")

        visible_book = Book.data.create(name="visible book", author=visible_author)
        visible_book.co_authors.add(visible_author)
        visible_book.co_authors.add(deleted_author)

        deleted_book = Book.data.create(name="deleted book", author=visible_author)
        deleted_book.co_authors.add(visible_author)
        deleted_book.co_authors.add(deleted_author)

        # deleted_author.delete()
        # deleted_author.delete()

        cls.visible_book = visible_book
        cls.visible_author = visible_author
        cls.deleted_book = deleted_book
        cls.deleted_author = deleted_author


class HideDeletedBooks(GeneralTestCase):
    def test_correct_visibility(self):
        self.assertEqual(self.visible_book.co_authors.count(), 2)
        self.deleted_author.delete()
        self.assertEqual(self.visible_book.co_authors.count(), 1)

        # TODO: the join sadly will include deleted data
        # we need some way to filter that out by default
        self.assertEqual(Book.data.filter(co_authors__name__contains="del").count(), 2)

        # but manually filtering still works of course
        self.assertEqual(
            Book.data.filter(
                co_authors__name__contains="del", co_authors__deleted__isnull=True
            ).count(),
            0,
        )

        self.assertEqual(Author.data.count(), 1)
        Author.data.all().delete()
        self.assertEqual(Author.data.count(), 0)

    def test_deleted_models_are_filtered_out_by_the_related_query_manager(self):

        self.assertEqual(Book.data.count(), 2)
        self.assertEqual(Author.data.count(), 2)

        self.deleted_author.delete()
        self.deleted_book.delete()

        self.assertEqual(Book.data.count(), 1)
        self.assertEqual(Author.data.count(), 1)

        self.assertEqual(self.visible_author.books.count(), 1)

    def test_undeleting_models(self):
        self.deleted_author.delete()
        self.assertEqual(Author.data.count(), 1)

        self.assertEqual(Author.data.deleted().count(), 1)
        Author.data.deleted().undelete()
        self.assertEqual(Author.data.deleted().count(), 0)
        self.assertEqual(Author.data.count(), 2)

        self.assertIsNotNone(Author.data.get(id=self.deleted_author.id))
        self.assertIsNotNone(Author.data.get(name=self.deleted_author.name))
        self.assertEqual(Author.data.filter(id=self.deleted_author.id).count(), 1)

    def test_hiding_models(self):

        Author.data.all().conceal()

        self.assertEqual(Author.data.count(), 2)
        self.assertEqual(Author.data.visible().count(), 0)

        Author.data.all().reveal()
        self.assertEqual(Author.data.visible().count(), 2)

    def test_deleted_data_is_still_accessible(self):

        self.deleted_author.delete()

        self.assertIsNotNone(Author.data.get(id=self.deleted_author.id))
        self.assertNotIn(self.deleted_author, Author.data.all())
        self.assertIn(self.visible_author, Author.data.all())

        with self.assertRaises(Author.DoesNotExist):
            Author.data.deleted().get(id=self.visible_author.id)


class RealDeletionTestCase(GeneralTestCase):
    def test_really_deleting_stuff(self):

        self.assertEqual(Author.data.count(), 2)
        self.assertEqual(Author.data.deleted().count(), 0)

        self.deleted_author.delete()

        self.assertEqual(Author.data.count(), 1)
        self.assertEqual(Author.data.deleted().count(), 1)

        self.deleted_author.delete(force=True)

        self.assertEqual(Author.data.count(), 1)
        self.assertEqual(Author.data.deleted().count(), 0)

        Author.data.all().delete(force=True)

        self.assertEqual(Author.data.count(), 0)
        self.assertEqual(Author.data.deleted().count(), 0)


class ModelTests(GeneralTestCase):
    def test_model_functions(self):
        self.assertEqual(str(self.visible_author), "visible")

    def test_pprint(self):
        self.assertIsNone(self.visible_author.pprint())


class ManagerQuerysetTest(TestCase):
    def test_queryset_methods(self):
        author = Author.data.create(name="visible")

        CoverBook.data.create(name="visible book", author=author)

        self.assertEqual(CoverBook.data.not_null().count(), 1)
        self.assertEqual(CoverBook.data.all().not_null().count(), 1)


class UndeleteTestCase(GeneralTestCase):
    def test_model_undelete(self):
        self.assertEqual(Author.data.count(), 2)
        self.deleted_author.delete()
        self.assertEqual(Author.data.count(), 1)
        self.deleted_author.undelete()
        self.assertEqual(Author.data.count(), 2)


class USerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = TestUser.data.create(
            username="tester",
            email="Tester@EXample.com",
            first_name="John",
            last_name="Doe",
        )

    def test_clean_email(self):

        self.user.clean()
        self.assertEqual(self.user.email, "Tester@example.com")

    def test_get_name(self):

        self.assertEqual(self.user.get_full_name(), "John Doe")
        self.assertEqual(self.user.get_short_name(), "John")

    def test_sending_email(self):

        self.user.email_user("foo", "bar")

        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, "foo")
        self.assertEqual(mail.outbox[0].recipients(), [settings.EMAIL_OVERRIDE_ADDRESS])

    @override_settings(EMAIL_OVERRIDE_ADDRESS=None)
    def test_really_sending_email(self):

        self.user.email_user("foo", "bar")

        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, "foo")
        self.assertEqual(mail.outbox[0].recipients(), [self.user.email])


class AppConfigTest(TestCase):
    def test_the_config(self):
        from django.apps import apps

        self.assertEqual(
            apps.get_app_config("django_undeletable").verbose_name,
            "Django undeletable models",
        )
