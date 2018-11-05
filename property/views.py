from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from django.forms import modelformset_factory, inlineformset_factory
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
from django.shortcuts import render, redirect, reverse
import random
from .models import Property, PropertyRating, MyProperty, Neighborhood, City, Category, Images
from .mixins import PropertyManagerMixin
from django.db.models import Count
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
from random import shuffle


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
    success_url = 'realtor:home'

    def get(self, request):
        Property_ImagesFormSet = modelformset_factory(Images, fields=('image',), extra=4, max_num=5)
        form = PropertyForm()
        formset = Property_ImagesFormSet(queryset=Images.objects.none())
        context = {'form':form, 'formset':formset}
        return render(request, self.template_name, context)
    
    def post(self, request, **kwargs):
        Property_ImagesFormSet = modelformset_factory(Images, fields=('image',), extra=4, max_num=5)
        form = PropertyForm(request.POST or None, request.FILES or None)
        formset = Property_ImagesFormSet(request.POST or None, request.FILES or None)
        
        
        if form.is_valid() :
            property = form.save(commit = False)
            tag = form.cleaned_data.get("tags")
            realtor = self.get_account()
            property.realtor = realtor
            property.save()
            if tag:
                tag_list = tag.split(",")
                for tag in tag_list:
                    if not tag == "":
                        new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                        new_tag.save()
                        new_tag.property.add(form.instance or None)
            
            if formset.is_valid():
                for f in formset:
                    try:
                        property_images = Images(property = property,image = f.cleaned_data['image'])
                        property_images.save()
                    except Exception as e:
                        break
            
            
            
            return redirect('realtor:home')
        
        
            
    


   
# PropertyManagerMixin, 

class PropertyUpdateView(PropertyManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
    model = Property
    template_name = "property/edit_property_form.html"
    form_class = PropertyForm

    success_url = "/property/"
    submit_btn = "Update Property"

    def get_context_data(self, **kwargs):
        context = super(PropertyUpdateView, self).get_context_data(**kwargs)
        Property_ImagesFormSet = modelformset_factory(Images, fields=('image',), extra=0)
        qs = Images.objects.filter(property=self.get_object())
        formset = Property_ImagesFormSet(queryset=qs)
        context['formset'] = formset
        return context

    def post(self, request, **kwargs):
        object = self.get_object()
        Property_ImagesFormSet = modelformset_factory(Images, fields=('image',))
        form = PropertyForm(request.POST, request.FILES, instance=object )
        formset = Property_ImagesFormSet(request.POST or None , request.FILES or None)
        
        
        if form.is_valid() :
            property = form.save(commit = False)
            tag = form.cleaned_data.get("tags")
            realtor = self.get_account()
            property.realtor = realtor
            property.save()
            obj = self.get_object()
            obj.tag_set.clear()
            if tag:
                tag_list = tag.split(",")
                for tag in tag_list:
                    if not tag == "":
                        new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                        new_tag.save()
                        new_tag.property.add(form.instance or None)
            
            if formset.is_valid():
                formset.save()
                # for f in formset:
                #     try:
                #         property_images = Images(property = property,image = f.cleaned_data['image'])
                #         property_images.save()
                #     except Exception as e:
                #         break
            
            return redirect('realtor:home')
 

    def get_initial(self):
        initial = super(PropertyUpdateView, self).get_initial()
        tags = self.get_object().tag_set.all()
        initial["tags"] = ", ".join([x.title for x in tags])

        return initial





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
       
        
        featured = list(Property.objects.filter(featured = True, city__slug = slug))

        shuffle(featured)

        context['featured'] = featured
        return context
   
class PropertyListView(TemplateView):
    
    template_name = "property/property_list.html"

    
    def get_context_data(self, *args, **kwargs):
        
        property_list = list(Property.objects.all())
        shuffle(property_list)
        paginator = Paginator(property_list, 10)
        page = self.request.GET.get('page')
        

        try:
            property = paginator.page(page)
        except PageNotAnInteger:
            property = paginator.page(1)
        except EmptyPage:
            property = paginator.page(paginator.num_pages)



        property_type  = Category.objects.all()
        city = City.objects.all().annotate(num_property = Count("property")).order_by("-num_property")
        featured = list(Property.objects.filter(featured = True))

        shuffle(featured)
        context = { 'property_type':property_type,
                    'city': city, 
                    'property':property,
                    'featured': featured }
        return context



class PropertyCategoryListView(ListView):
    template_name = "property/property_category_listview.html"
    queryset      = Category.objects.all()[:6]


def get_city(request, slug, **kwargs):
    city_property_list = list(Property.objects.filter(city__slug=slug))
    shuffle(city_property_list)
    paginator = Paginator(city_property_list, 10)
    page = request.GET.get('page')
        

    try:
        city_property = paginator.page(page)
    except PageNotAnInteger:
        city_property = paginator.page(1)
    except EmptyPage:
        city_property = paginator.page(paginator.num_pages)


    


    
    neigborhood_name = Neighborhood.objects.filter(city__slug=slug).annotate(num_property = Count("property")).order_by("-num_property")
    property_type  = Category.objects.all()
    city_name = City.objects.filter(slug=slug)[:1]
    
   
    featured = list(Property.objects.filter(featured = True,city__slug=slug))
    shuffle(featured)
    context = { 'city_property' : city_property,
                'neigborhood_name':neigborhood_name,
                'property_type':property_type,
                'featured': featured ,
                'city_name':city_name
                 }
    return render(request,'property/property_city_detailview.html', context)


def get_neighborhood(request, slug, neighborhood_slug):
    neighborhood_property_list = list(Property.objects.filter(city__slug=slug, neighborhood__slug = neighborhood_slug))
    shuffle(neighborhood_property_list)
    paginator = Paginator(neighborhood_property_list, 10)
    page = request.GET.get('page')
        

    try:
        neighborhood_property = paginator.page(page)
    except PageNotAnInteger:
        neighborhood_property = paginator.page(1)
    except EmptyPage:
        neighborhood_property = paginator.page(paginator.num_pages)


    
    city_neigborhoods = Neighborhood.objects.filter(city__slug=slug).annotate(num_property = Count("property")).order_by("-num_property")
    featured = list(Property.objects.filter(featured = True,city__slug=slug, neighborhood__slug = neighborhood_slug))
    property_type  = Category.objects.filter()
    neigborhood_name = Neighborhood.objects.filter(city__slug=slug, slug=neighborhood_slug)[:1]
    # city =  city_name = City.objects.filter(slug=slug)[:1]

    shuffle(featured)

    city = City.objects.filter(slug=slug)[:1]
    context = {  
        'neighborhood_property' : neighborhood_property , 
        'city_neigborhoods' : city_neigborhoods,
        'property_type':property_type,
        'featured':featured,
        'neigborhood_name':neigborhood_name,
        'city': city
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






