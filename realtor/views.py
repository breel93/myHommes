from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import View, UpdateView, DetailView, ListView
from django.views.generic.edit import FormMixin
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





class RealtorDetailRedirectView(RedirectView):
    permanent = True
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Property, pk=kwargs['pk'])
        return obj.get_absolute_url()


class RealtorView(RealtorAccountMixin, FormMixin, View):
    # form_class = NewRealtorForm
    template_name = "realtor/index.html"
    success_url = 'realtor:home'

  
    def post(self, request, **kwargs):
        apply_form = NewRealtorForm(request.POST, request.FILES)
        if apply_form.is_valid():
            realtor = apply_form.save(commit = False)
            realtor.user = request.user
            realtor.save()
        else:
            return redirect('realtor:home')
        return redirect('realtor:home')
        # context = {'form':form}
        # return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
      
        # apply_form = self.get_form()
        apply_form = NewRealtorForm()
        account = Realtor.objects.filter(user=self.request.user)
        exists = account.exists()
        active = None
        context = {}

        if exists:
            account = account.first()
            active = account.active

        if not exists and not active:
            context["title"] = "Apply for Account"
            context["apply_form"] = apply_form
        elif exists and not active:
            context["title"] = "Account Pending"
        elif exists and active:
            context["title"] = "Realtor"
            # property = Property.objects.filter(realtor=account)
            property = self.get_property().order_by('-timestamp')
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

class RealtorUpdate(RealtorAccountMixin, UpdateView):
    model = Realtor
    template_name = 'realtor/updateform.html'
    form_class = NewRealtorForm
    success_url = reverse_lazy('realtor:home')

  

        

class RealtorsListView(ListView):
    template_name = "realtor/realtor_list.html"
    queryset      = Realtor.objects.all()[:50]

class RealtorsDetailView(DetailView):
    queryset = Realtor.objects.all()
    template_name = "realtor/realtor_detail.html"
