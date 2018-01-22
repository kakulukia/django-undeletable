from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_undeletable.models import NamedModel, BaseModel, AbstractUser


class Author(NamedModel):
    pass


class Book(NamedModel):
    author = models.ForeignKey(Author, related_name='books', null=True,
                               related_query_name='author', on_delete=models.SET_NULL)
    co_authors = models.ManyToManyField(Author, related_name='featured_books',
                                        related_query_name='co_author')


class TestUser(AbstractUser):
    groups = None
    user_permissions = None

    class Meta(BaseModel.Meta):
        verbose_name = _('user')
        verbose_name_plural = _('users')
