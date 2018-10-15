from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from real.utils import unique_slug_generator

# Create your models here.

from property.models import Property




class TagQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)


class TagManager(models.Manager):
	def get_queryset(self):
		return TagQuerySet(self.model, using=self._db)

	def all(self, *args, **kwargs):
		return super(TagManager, self).all(*args, **kwargs).active()


class Tag(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug =  models.SlugField(unique=True, blank=True)
    property = models.ManyToManyField(Property, blank=True)
    active  = models.BooleanField(default=True)

    objects = TagManager()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        view_name = "tag:detail"
        return reverse(view_name,kwargs={"slug": self.slug})




   



def tag_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)
		
pre_save.connect(tag_pre_save_receiver, sender=Tag)



