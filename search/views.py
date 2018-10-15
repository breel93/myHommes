from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from property.models import Property
# Create your views here.


class SearchPropertyListView(ListView):
    # queryset = Product.objects.all()
    template_name = "search/search_list.html"

    def  get_context_data(self, *args, **kwargs):
        context = super(SearchPropertyListView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:
            return Property.objects.search(query)
        return Property.objects.featured()
        '''
        __icontains = field contains this
        __iexact = fields is exactly this
        '''