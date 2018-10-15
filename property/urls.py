from django.conf.urls import url

from .views import (
        PropertyListView, 
        PropertyDetailSlugView, 
        PropertyCreateView,
        PropertyUpdateView,
        PropertyRatingView,
        UserFavoriteProperty,
        # ContactView,
        # AboutView
)
from .import views



app_name = 'property'

urlpatterns = [
    url(r'^$',PropertyListView.as_view(),name='list'),
    # url(r'^create/$',views.create_property,name='create'),
    url(r'^(?P<slug>[\w-]+)/$',PropertyDetailSlugView.as_view(),name='details'),
    url(r'^(?P<slug>[\w-]+)/edit/$',PropertyUpdateView.as_view(),name='edit'),
    url(r'^ajax/rating/$', PropertyRatingView.as_view(), name='ajax_rating'),
    url(r'^city/(?P<slug>[\w-]+)/$', views.get_city, name ="city"),
    url(r'^city/(?P<slug>[\w-]+)/(?P<neighborhood_slug>[\w-]+)/$', views.get_neighborhood, name ="neighborhood"),
]
