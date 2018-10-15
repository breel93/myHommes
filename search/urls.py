from django.conf.urls import url

from property import views
from search.views import SearchPropertyListView

app_name = 'search'


urlpatterns =[
     url(r'^$',SearchPropertyListView.as_view(),name='search-query'),
#      url(r'^/(?P<pk>\d+)/$',ProductDetailView.as_view(),name='product-details'),
     
]