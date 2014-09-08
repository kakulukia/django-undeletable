# coding=utf-8
from django.db.models.query import QuerySet
from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core import validators


# basic model stuff
##########################################
class DataQuerySet(QuerySet):
    def delete(self):
        self.update(active=False, deleted=timezone.now())


class AllObjectsQuerySet(QuerySet):
    def undelete(self):
        self.update(active=True, deleted=None)


class DataManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        qs = DataQuerySet(self.model, using=self._db)
        return qs.filter(active=True)

    def delete(self):
        self.update(active=False, deleted=timezone.now())


class AllObjectsManager(models.Manager):

    def get_queryset(self):
        return DataQuerySet(self.model, using=self._db)

    def deleted(self):
        return self.filter(active=False)


# base model with useful stuff
class BaseModel(models.Model):

    created = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    modified = models.DateTimeField(auto_now=True, editable=False, db_index=True)
    deleted = models.DateTimeField(editable=False, null=True)

    active = models.BooleanField(default=True, editable=False, db_index=True)

    # access only active data objects
    data = DataManager()
    # access all (including deleted) data
    objects = AllObjectsManager()

    class Meta:
        abstract = True
        ordering = ['-created']

    # deleted data is bad - doing it you shouldn't!
    def delete(self, using=None):
        self.active = False
        self.save()

    def undelete(self, using=None):
        self.active = True
        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.active:
            self.deleted = None
        elif not self.deleted:
            self.deleted = timezone.now()

        super(BaseModel, self).save(force_insert=force_insert, using=using,
                                    update_fields=update_fields)

    def reload_me(self):
        if self.id:
            return self.__class__.objects.get(id=self.id)


class NamedModel(BaseModel):
    name = models.CharField('Name', max_length=150, db_index=True)

    class Meta:
        ordering = ['name']
        abstract = True

    def __unicode__(self):
        return self.name


class UserDataManager(UserManager, DataManager):
    pass


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_('user.login.username_help'),
                                validators=[
                                    validators.RegexValidator(
                                        r'^[\w.@+-]+$', _('forms.errors.enter_valid_username.'), 'username_invalid')
                                ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    data = UserDataManager()
    objects = UserManager()

    class Meta:
        abstract = True
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """ Returns the first_name plus the last_name, with a space in between. """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """ Returns the short name for the user. """
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
