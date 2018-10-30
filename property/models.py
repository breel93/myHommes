from django.db.models import Q

import random
from django.conf import settings
import os
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from real.utils import unique_slug_generator
from main.models import User
from realtor.models import Realtor






def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext



def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "property/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )




class City(models.Model):
    title        = models.CharField(max_length=120, blank=True, unique=True)
    image        = models.ImageField(upload_to='properties/', null=True, blank=True)
    slug         = models.SlugField(blank=True,unique=True)
    
    


    def get_city_url(self):
        return reverse("property:city", kwargs={"slug": self.slug})

    def __str__(self):
        return self.slug
    
    
    def get_property(self):
        return property.objects.filter(city__title = self.title)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


def city_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(city_pre_save_receiver, sender=City)



class CityImage(models.Model):
    city = models.ForeignKey(City, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='city/', null=True, blank=True)

    def __str__(self):
        return self.city



# neighborhood
class Neighborhood(models.Model):
    title        = models.CharField(max_length=120, blank=True, unique=True)
    image        = models.ImageField(upload_to='properties/', null=True, blank=True)
    slug         = models.SlugField(blank=True,unique=True)
    city         = models.ForeignKey(City,blank=True, default=1, max_length=300, unique=False, on_delete=models.CASCADE)
    

    def get_neighborhood_url(self):
        return reverse("property:neighborhood", kwargs={"slug": self.city,"neighborhood_slug": self.slug})

    # def class_name(self):
    #     return self.__class__.__name__

    def __str__(self):
        return self.slug
    
    
   
    
    
    def get_property(self):
        return property.objects.filter(neighborhood__title = self.title)

    class Meta:
        verbose_name = 'Neighborhood'
        verbose_name_plural = 'Neighborhoods'


def neighborhood_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(neighborhood_pre_save_receiver, sender=Neighborhood)

class NeighborhoodImage(models.Model):
    neighborhood = models.ForeignKey(Neighborhood, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='neigborhood/', null=True, blank=True)

    def __str__(self):
        return self.neighborhood

class Category(models.Model):
    title        = models.CharField(max_length=120, blank=True, unique=True)
    slug         = models.SlugField(blank=True,unique=True)

    def get_category_url(self):
        return reverse("property:category-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.slug
    
    
    def get_property(self):
        return property.objects.filter(category__title = self.title)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(category_pre_save_receiver, sender=Category)



class PropertyQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(description__icontains=query)  # |
                   # Q(tag__title__icontains=query)
                   )
        return self.filter(lookups).distinct()


class PropertyManager(models.Manager):
    def get_queryset(self):
        return PropertyQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


STOREY = (
    ('Bungalow', 'Bungalow'),
    ('Duplex', 'Duplex'),
    ('One Storeys', 'One Storeys'),
    ('Two Storeys', 'Two Storeys'),
    ('Three Storeys', 'Three Storeys'),
    ('Four Storeys', 'Four Storeys'),
    ('Five Storeys', 'Five Storeys'),
)



FURNISHED = (
    ('yes', 'yes'),
    ('no', 'no'),
    ('somewhat', 'somewhat'),
)

NEW_PROPERTY = (
    ('yes', 'yes'),
    ('no', 'no'),
)

PARKING_SPACE = (
    ('yes', 'yes'),
    ('no', 'no'),
)

BEDROOM = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
)

DURATION = (
    ('1 month', '1 month'),
    ('3 months', '3 months'),
    ('6 months', '6 months'),
    ('Year', 'Year'),
    ('2 Years', '2 Years'),
    ('3 Years', '3 Years'),
    
)

BATHROOM = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
)
PURPOSE = (
    ('Residential', 'Residential'),
    ('Office', 'Office'),
    ('Business', 'Business'),
    ('Other', 'Other'),
)


class Property(models.Model):
    # realtor = models.ForeignKey(User, related_name='property')
    realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    address = models.CharField(blank=True, max_length=300)
    neighborhood = models.ForeignKey(Neighborhood,blank=True,default="", max_length=300, unique=False, on_delete=models.CASCADE)
    city = models.ForeignKey(City,blank=True, default="", max_length=300, unique=False, on_delete=models.CASCADE)
    storey = models.CharField(_('storey'), blank=True, max_length=300,
                              choices=STOREY, unique=False)

    category = models.ForeignKey(Category, default="", max_length=300, unique=False, on_delete=models.CASCADE)

    bedroom = models.CharField(_('bed'), max_length=300,
                               choices=BEDROOM, unique=False)

    bathroom = models.CharField(_('bathroom'), max_length=300,
                                choices=BATHROOM, unique=False)

    description = models.TextField()

    furnished = models.CharField(_('furnished'), blank=True, max_length=300,
                                 choices=FURNISHED, unique=False)
    parking_space = models.CharField(_('parking_space'), blank=True, max_length=300,
                                     choices=PARKING_SPACE, unique=False)

    new_property = models.CharField(_('new_property'), blank=True, max_length=300,
                                    choices=NEW_PROPERTY, unique=False)

    purpose = models.CharField(_('purpose'), blank=True, max_length=300,
                               choices=PURPOSE, unique=False)
    
    duration = models.CharField(_('duration'), blank=True, max_length=300,
                               choices=DURATION, unique=False)

    square_meter = models.DecimalField(blank=True, decimal_places=2, max_digits=20, default=0.00)
    price = models.DecimalField(decimal_places=0, max_digits=20, default=0.00)
    main_image = models.ImageField(upload_to='properties/', null=True, blank=True)
    main_image_two  = models.ImageField(upload_to='properties/',  null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PropertyManager()

    def __str__(self):
        return self.slug

    @property
    def name(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("property:details", kwargs={"slug": self.slug})
    
    def get_edit_url(self):
        return reverse("realtor:property_edit", kwargs={"pk": self.id})

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Property'


class Images(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='properties/', null=True, blank=True)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
    def __str__(self):
        return self.property.title

# def create_more_images(sender, **kwarg):
#     if kwarg ['created']:
#         property_images = Images.objects.create(user=kwarg['instance'])

# post_save.connect(create_more_images, sender=Property) 


class MyProperty(models.Model):
    user = models.OneToOneField(User)
    property = models.ManyToManyField(Property, blank=True)

    def __str__(self):
        return self.property.count



def property_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(property_pre_save_receiver, sender=Property)


class PropertyRating(models.Model):
    user = models.ForeignKey(User)
    property = models.ForeignKey(Property)
    rating = models.IntegerField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.property.count

