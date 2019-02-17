from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_undeletable.models import (
    NamedModel,
    BaseModel,
    AbstractUser,
    DataQuerySet,
    DataManager,
)


class Author(NamedModel):
    pass


class Book(NamedModel):
    author = models.ForeignKey(
        Author,
        related_name="books",
        null=True,
        related_query_name="author",
        on_delete=models.SET_NULL,
    )
    co_authors = models.ManyToManyField(
        Author, related_name="featured_books", related_query_name="co_author"
    )


class BookQuerySet(DataQuerySet):
    def not_null(self):
        return self.filter(author__isnull=False)


class CoverBook(Book):
    data = DataManager.from_queryset(BookQuerySet)()


class TestUser(AbstractUser):
    groups = None
    user_permissions = None

    class Meta(BaseModel.Meta):
        verbose_name = _("user")
        verbose_name_plural = _("users")
