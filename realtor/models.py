# # from property.models import Property
# from django.apps import apps
from django.conf import settings
from django.db import models
from main.models import User
from django.db.models.signals import post_save
from django.urls import reverse








class Realtor(models.Model):
    user = models.OneToOneField(User)
    city = models.ForeignKey('property.City', default=1)
    managers = models.ManyToManyField(User, related_name="manager_realtor", blank=True)
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    image = models.ImageField(upload_to='realtor/', null=True, blank=True)
    address = models.CharField(blank=True,max_length=200)
    state = models.CharField(blank=True,max_length=200)
    phone_number = models.IntegerField(blank=True,default='0')
    website  = models.URLField(blank=True,max_length=200)
    company_name = models.CharField(blank=True,max_length=200)
    agree_to_terms = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name
    
    def get_realtor_url(self):
        return reverse("realtor:realtor-detail", kwargs={"pk":self.pk})

# def realtor_profile(sender, **kwargs):
#     if kwargs['created']:
#         user_profile = Realtor.objects.create(user=kwargs['realtor'])
# post_save.connect(realtor_profile,sender=User)