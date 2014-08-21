# coding=utf-8
from django.db import models
from django.db.models.query import QuerySet
from django.utils.datetime_safe import datetime

# basic model stuff
##########################################
class DataQuerySet(QuerySet):
    def delete(self):
        self.update(active=False, deleted=datetime.now())


class AllObjectsQuerySet(QuerySet):
    def undelete(self):
        self.update(active=True, deleted=None)


class DataManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self):
        qs = DataQuerySet(self.model, using=self._db)
        return qs.filter(active=True)

    def delete(self):
        self.update(active=False, deleted=datetime.now())


class AllObjectsManager(models.Manager):

    def get_query_set(self):
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
            self.deleted = datetime.now()

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
