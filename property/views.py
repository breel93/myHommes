from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch

# Create your views here.
from django.shortcuts import render, redirect, reverse
import random
from .models import Property, PropertyRating, MyProperty, Neighborhood, City, Category
from .mixins import PropertyManagerMixin
from tag.models import Tag
from analytics.models import TagView
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from real.mixins import (
    LoginRequiredMixin,
    MultiSlugMixin,
    SubmitBtnMixin
)

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    TemplateView
)

from .forms import PropertyForm
from realtor.mixins import RealtorAccountMixin
from real.mixins import AjaxRequiredMixin
from realtor.models import Realtor


# Create your views here.
class PropertyRatingView(AjaxRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({}, status=401)
        # credit card required **

        user = request.user
        property_id = request.POST.get("property_id")
        rating_value = request.POST.get("rating_value")
        exists = Property.objects.filter(id=property_id).exists()
        if not exists:
            return JsonResponse({}, status=404)

            property

        try:
            property_obj = Property.object.get(id=property_id)
        except:
            property_obj = Property.objects.filter(id=property_id).first()

        rating_obj, rating_obj_created = PropertyRating.objects.get_or_create(
                user=user,
                property=property_obj
                )
        try:
            rating_obj = PropertyRating.objects.get(user=user, property=property_obj)
        except PropertyRating.MultipleObjectsReturned:
            rating_obj = PropertyRating.objects.filter(user=user, property=property_obj).first()
        except:

            rating_obj = PropertyRating()
            rating_obj.user = user
            rating_obj.property = property_obj
        rating_obj.rating = int(rating_value)
        myproperty = user.mypropertys.property.all()

        if property_obj in myproperty:
            rating_obj.verified = True
        # verify ownership
        rating_obj.save()

        data = {
            "success": True
        }
        return JsonResponse(data)






class PropertyCreateView(RealtorAccountMixin, SubmitBtnMixin, CreateView):
    template_name = "property/create_property_form.html"
    form_class = PropertyForm
    success_url = 'realtor:home'

    def form_valid(self, form):
        realtor = self.get_account()
        form.instance.realtor = realtor
        valid_data = super(PropertyCreateView, self).form_valid(form)
        # form.instance.managers.add(user)
        # add all default users
        tag = form.cleaned_data.get("tags")
        if tag:
            tag_list = tag.split(",")
            for tag in tag_list:
                if not tag == "":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.property.add(form.instance)
        return valid_data

   
   
# PropertyManagerMixin, 

class PropertyUpdateView(PropertyManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
    model = Property
    template_name = "property/edit_property_form.html"
    form_class = PropertyForm
    success_url = "/property/"
    submit_btn = "Update Property"



    def get_initial(self):
        initial = super(PropertyUpdateView, self).get_initial()
        tags = self.get_object().tag_set.all()
        initial["tags"] = ", ".join([x.title for x in tags])

        return initial

    def form_valid(self, form):
        valid_data = super(PropertyUpdateView, self).form_valid(form)

        tags = form.cleaned_data.get("tags")
        obj = self.get_object()
        obj.tag_set.clear()
        if tags:
            tags_list = tags.split(",")

            for tag in tags_list:
                if not tag == " ":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.property.add(self.get_object())
        return valid_data






class RealtorPropertyListView(RealtorAccountMixin, ListView):
    model = Property
    template_name = "realtor/property_list_view.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(RealtorPropertyListView, self).get_queryset(**kwargs)
        qs = qs.filter(realtor=self.get_account())
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                    Q(title__icontains=query)|
                    Q(description__icontains=query)
                ).order_by("title")
        return qs




class PropertyDetailSlugView(DetailView):
    queryset = Property.objects.all()
    template_name = "property/property_details.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PropertyDetailSlugView, self).get_context_data(*args, **kwargs)
        slug = self.kwargs.get('slug')
        obj = self.get_object()
        tags = obj.tag_set.all()
        if self.request.user.is_authenticated():
            for tag in tags:
                new_view = TagView.objects.add_count(self.request.user, tag)
       
        
        context['featured'] = Property.objects.filter(featured = True)[:6]
        
        return context
   
class PropertyListView(TemplateView):
    # queryset = Property.objects.all()
    template_name = "property/property_list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(PropertyListView, self).get_context_data(*args, **kwargs)
    #     print(dir(context.get('page_obj'))) .order_by('-created')
    #     return context
    def get_context_data(self, *args, **kwargs):
        property = Property.objects.all()[:50]
        property_type  = Category.objects.all()
        city = City.objects.all()[:10]
        featured = Property.objects.filter(featured = True)[:3]

        context = { 'property_type':property_type,
                    'city': city, 
                    'property':property,
                    'featured': featured }
        return context



class PropertyCategoryListView(ListView):
    template_name = "property/property_category_listview.html"
    queryset      = Category.objects.all()[:6]


def get_city(request, slug):
    city_property = Property.objects.filter(city__slug=slug)
    neigborhood_name = Neighborhood.objects.filter(city__slug=slug)
    property_type  = Category.objects.all()
    # queryset   = Category.objects.filter(slug = category_name)
    featured = Property.objects.filter(featured = True,city__slug=slug)[:3]
    context = { 'city_property' : city_property,
                'neigborhood_name':neigborhood_name,
                'property_type':property_type,
                'featured': featured 
                 }
    return render(request,'property/property_city_detailview.html', context)


def get_neighborhood(request, slug, neighborhood_slug):
    neighborhood_property = Property.objects.filter(city__slug=slug, neighborhood__slug = neighborhood_slug)
    neigborhood_name = Neighborhood.objects.filter(city__slug=slug)
    featured = Property.objects.filter(featured = True,city__slug=slug, neighborhood__slug = neighborhood_slug)[:3]
    property_type  = Category.objects.all()
    context = {  
        'neighborhood_property' : neighborhood_property , 
        'neigborhood_name' : neigborhood_name,
        'property_type':property_type,
         'featured':featured
         }
    return render(request, 'property/property_neighborhood_detail.html',context)







class UserFavoriteProperty(LoginRequiredMixin, ListView):
	model = MyProperty
	template_name = "property/favorite_list.html"

	def get_queryset(self, *args, **kwargs):
		obj = MyProperty.objects.get_or_create(user=self.request.user)[0]
		qs = obj.property.all()
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("title")
		return qs






# class RealtorsListView(ListView):
# 	model = Property
# 	template_name = "products/realtor_list.html"

# 	def get_object(self):
# 		ema= self.kwargs.get("email")
# 		seller = get_object_or_404(Realtor, user__username=username)
# 		return seller

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(RealtorsListView, self).get_context_data(*args, **kwargs)
# 		context["vendor_name"] = str(self.get_object().user.username)
# 		return context

# 	def get_queryset(self, *args, **kwargs):
# 		seller = self.get_object()
# 		qs = super(VendorListView, self).get_queryset(**kwargs).filter(seller=seller)
# 		query = self.request.GET.get("q")
# 		if query:
# 			qs = qs.filter(
# 					Q(title__icontains=query)|
# 					Q(description__icontains=query)
# 				).order_by("title")
# 		return qs