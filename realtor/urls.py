from django.conf.urls import include, url
from django.contrib import admin
from property.views import PropertyCreateView
from property.views import RealtorPropertyListView
from property.views import PropertyUpdateView #PropertyOtherImages
from .import views


from .views import (
        RealtorView,
        RealtorDetailRedirectView,
        # Realtor_Profile,
        RealtorUpdate,
        RealtorsListView,
        RealtorsDetailView,
        RealtorCreate

        
        )

urlpatterns = [ 
    url(r'^$', RealtorView.as_view(), name='home'),
    url(r'^create/$', RealtorCreate.as_view(), name='create_reator'),
    url(r'^update/(?P<pk>\d+)/$', RealtorUpdate.as_view(), name='update'),
    url(r'^property/$',RealtorPropertyListView.as_view(),name='property_list'),
    url(r'^property/create/$',PropertyCreateView.as_view(),name='create'),
    # url(r'^property/add-more-images/$',PropertyOtherImages.as_view(),name='add_more_images'),
    url(r'^property/(?P<pk>\d+)/edit/$',PropertyUpdateView.as_view(),name='property_edit'),
    url(r'^property/(?P<pk>\d+)/$',RealtorDetailRedirectView.as_view()),
    url(r'^realtors/$', RealtorsListView.as_view(), name='realtors'),
    url(r'^realtors/(?P<pk>\d+)/$', RealtorsDetailView.as_view(), name='realtor-detail'),
   # url(r'^realtor_profile/(?P<pk>\d+)/$', Realtor_Profile.as_view(), name='realtor_profile')
    # url(r'^realtor_profile/$', views.realtor_profile, name='realtor_profile')
] 