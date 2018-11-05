from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import View, UpdateView, DetailView, ListView, CreateView

from .forms import NewRealtorForm
from real.mixins import LoginRequiredMixin
# Create your views here.
from .models import Realtor
from main.models import User
from property.models import Property
from .mixins import RealtorAccountMixin
from django.views.generic.base import RedirectView
from real.mixins import SubmitBtnMixin
from real.mixins import (
    LoginRequiredMixin,
    MultiSlugMixin,
    SubmitBtnMixin
)
from django.db.models import Count

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from random import shuffle



class RealtorDetailRedirectView(RedirectView):
    permanent = True
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Property, pk=kwargs['pk'])
        return obj.get_absolute_url()


class RealtorView(RealtorAccountMixin, View):
    
    template_name = "realtor/index.html"
    
    def get(self, request, *args, **kwargs):
      
        
        account = Realtor.objects.filter(user=self.request.user)
        exists = account.exists()
        active = None
        context = {} 

        if exists:
            account = account.first()
            active = account.active

        if exists and not active:
            context["title"] = "Account Pending"
        elif exists and active:
            context["title"] = "Realtor"
            # property = Property.objects.filter(realtor=account)
            property_list = self.get_property().order_by('-timestamp')
            shuffle(property_list)
            paginator = Paginator(property_list, 10)
            page = self.request.GET.get('page')
            

            try:
                property = paginator.page(page)
            except PageNotAnInteger:
                property = paginator.page(1)
            except EmptyPage:
                property = paginator.page(paginator.num_pages)

            
            context["property"] = property
           
        else:
            pass

        return render(request, "realtor/index.html", context)

    # def form_valid(self, form):
    #     valid_data = super(RealtorView, self).form_valid(form)
    #     obj = Realtor.objects.create(user=self.request.user)
    #     return valid_data

    # def form_invalid(self, form):
    #         pass

class RealtorCreate(CreateView, SubmitBtnMixin):
    template_name = "realtor/create_realtor.html"
    success_url = 'realtor:home'
    form = NewRealtorForm()

    def get(self, request, *args, **kwargs):
        # apply_form = self.get_form()
        context = {} 
        form = NewRealtorForm()
        context["title"] = "Apply for Account"
        context["apply_form"] = form
        return render(request, "realtor/create_realtor.html", context)


    def post(self, request, **kwargs):
        form = NewRealtorForm(request.POST, request.FILES or None)
        if form.is_valid():
            realtor = form.save(commit = False)
            realtor.user = request.user
            realtor.save()
        else:
            return redirect('realtor:create_reator')
        return redirect('realtor:home')
        # context = {'form':form}
        # return render(request, self.template_name, context)
    def form_valid(self, form):
        valid_data = super(RealtorView, self).form_valid(form)
        obj = Realtor.objects.create(user=self.request.user)
        return valid_data
    



class RealtorUpdate(RealtorAccountMixin, UpdateView):
    model = Realtor
    template_name = 'realtor/updateform.html'
    form_class = NewRealtorForm
    success_url = reverse_lazy('realtor:home')

  

        

class RealtorsListView(ListView):
    template_name = "realtor/realtor_list.html"
    queryset      = Realtor.objects.all().annotate(num_property = Count("property")).order_by("-num_property")
    paginate_by = 12
    context_object_name = 'realtors'


    

class RealtorsDetailView(DetailView):
    queryset = Realtor.objects.all().annotate(num_property = Count("property")).order_by("-num_property")
    
    template_name = "realtor/realtor_detail.html"
    def get_context_data(self,*args, **kwargs):
        context = super(RealtorsDetailView, self).get_context_data(*args, **kwargs)
        realtor_id = self.kwargs['pk']
        realtor_property_list = list(Property.objects.filter(realtor__id=realtor_id))
        shuffle(realtor_property_list)
        paginator = Paginator(realtor_property_list, 12)
        page = self.request.GET.get('page')
        

        try:
            realtor_property = paginator.page(page)
        except PageNotAnInteger:
            realtor_property = paginator.page(1)
        except EmptyPage:
            realtor_property = paginator.page(paginator.num_pages)

        
        context['realtor_property'] = realtor_property
        return context
    
    
