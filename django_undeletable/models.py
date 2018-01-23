# coding=utf-8
from __future__ import absolute_import, unicode_literals

from pprint import pprint

from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.db.models.query import QuerySet
from django.db.models.signals import pre_delete, post_delete
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


# basic model managers
##########################################
class DataQuerySet(QuerySet):
    def delete(self, force=False):
        if force:
            return super(DataQuerySet, self).delete()
        else:
            # otherwise this list will be different in the next loop :)
            to_be_notified = list(self)
            for obj in to_be_notified:
                pre_delete.send(sender=self.model, instance=obj, using=self._db)

            qs = self.update(deleted=now())

            for obj in to_be_notified:
                post_delete.send(sender=self.model, instance=obj, using=self._db)

            return qs

    def undelete(self):
        self.update(deleted=None)

    def conceal(self):
        """
        Some times you just want to be able to hide stuff from the public eye.
        Use the visible manager method for your views instead to filter the data.
        """
        self.update(concealed=True)

    def reveal(self):
        self.update(concealed=False)


class DataManager(models.Manager):
    # use_for_related_fields = True

    def get_queryset(self):
        qs = self.get_full_queryset()
        return qs.filter(deleted__isnull=True)

    def get_full_queryset(self):
        return DataQuerySet(self.model, using=self._db)

    def get(self, *args, **kwargs):
        if "pk" in kwargs or "id" in kwargs:
            # because models are not deleted foreign keys might reference 'deleted data'
            # to not crash the admin in these cases, we let it still access this data
            # if explicitly asked for by id
            return self.get_full_queryset().get(*args, **kwargs)
        return self.get_queryset().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        if "pk" in kwargs or "id" in kwargs:
            return self.get_full_queryset().filter(*args, **kwargs)
        return self.get_queryset().filter(*args, **kwargs)

    def deleted(self):
        return self.get_full_queryset().filter(deleted__isnull=False)

    def visible(self):
        return self.filter(concealed=False)


# base model with useful stuff
##########################################
class BaseModel(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True, editable=False, db_index=True)
    modified = models.DateTimeField(auto_now=True, editable=False)
    deleted = models.DateTimeField(editable=False, null=True)

    # ability to hide stuff publicly
    concealed = models.BooleanField(default=False, editable=False)

    # access non deleted data only
    data = DataManager()
    objects = DataManager()  # fallback for 3rd party libs not respecting the default manager

    class Meta:
        abstract = True
        ordering = ['-created']
        get_latest_by = 'created'
        base_manager_name = 'data'
        default_manager_name = 'data'

    # deleted data is bad - doing it you shouldn't! (but if u really want, u can)
    def delete(self, using=None, force=False):
        if force:
            super(BaseModel, self).delete(using=using)
        else:
            model_class = type(self)
            pre_delete.send(sender=model_class, instance=self, using=self._state.db)
            self.deleted = now()
            self.save()
            post_delete.send(sender=model_class, instance=self, using=self._state.db)

    def undelete(self):
        # the model cannot just be saved since its not visible to Django
        # and thus it will come to the conclusion that new data has to be inserted
        self._meta.model.data.deleted().filter(id=self.id).update(deleted=None)

    def pprint(self):
        pprint(self.__dict__)


class NamedModel(BaseModel):
    name = models.CharField(_('Name'), max_length=150, db_index=True)

    class Meta(BaseModel.Meta):
        ordering = ['name']
        abstract = True

    def __str__(self):
        return self.name


class UserDataManager(UserManager, DataManager):
    pass


# abstract base user with data manager
# please copy this user definition into your code and enhance it as needed
############################################################################
class AbstractUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, email and  password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    data = UserDataManager()
    objects = UserDataManager()  # this should stay due to compatibilty issues with 3rd party libs

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta(BaseModel.Meta):
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super(AbstractBaseUser, self).clean()
        self.email = self.__class__.data.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=settings.DEFAULT_FROM_EMAIL, **kwargs):
        """
         Sends an email to this User.
         If settings.EMAIL_OVERRIDE_ADDRESS is set, this mail will be redirected to the alternate mail address.

        """
        receiver = self.email
        if settings.EMAIL_OVERRIDE_ADDRESS:
            receiver = settings.EMAIL_OVERRIDE_ADDRESS

        send_mail(subject, message, from_email, [receiver], **kwargs)
