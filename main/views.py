from django.shortcuts import render
from django.utils.http import is_safe_url
from django.views.generic import TemplateView, CreateView, FormView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count
from .models import User

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from .forms import RegistrationForm, UpdateCustomerForm, UpdateCustomerFormTwo, LoginForm
from .signals import user_logged_in
from .mixins import LoginRequiredMixin
import random

from django.views.generic import View
from django.shortcuts import render

# Create your views here.

from property.models import Property, City
from random import shuffle
import random


# Create your views here.

# class IndexView(TemplateView):
#     template_name = 'main/index.html'


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)  # from our registration form class in form.py, we get the request method

        if form.is_valid():
            form.save()

            email = request.POST.get('email')
            password = request.POST.get('password1')

            user = authenticate(
                request,
                email=email,
                password=password
            )
            login(request, user)
            return redirect(reverse('main:index'))
    else:
        form = RegistrationForm()
    args = {'form': form}
    return render(request, 'main/reg_form.html', args)


def user_profile(request):
    if request.method == "POST":
        form = UpdateCustomerForm(request.POST, instance=request.user, prefix='form')
        form2 = UpdateCustomerFormTwo(request.POST, instance=request.user.userprofile, prefix='form2')

        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect(reverse('main:profile'))
        else:
            return render(request, 'main/profile.html', {'form': form, 'form2': form2})
    else:
        form = UpdateCustomerForm(instance=request.user, prefix='form')
        form2 = UpdateCustomerFormTwo(instance=request.user.userprofile, prefix='form2')
        args = {'form': form, 'form2': form2}
        return render(request, 'main/profile.html', args)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your new password has been saved")
            update_session_auth_hash(request, form.user)
            return redirect(reverse('main:profile'))

    else:
        form = PasswordChangeForm(user=request.user)
    args = {'form': form}
    return render(request, 'main/change_password.html', args)


# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         "form": form
#     }

#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         print(form.cleaned_data)
#         email  = form.cleaned_data.get("email")
#         password  = form.cleaned_data.get("password")
#         user = authenticate(request, email=email, password=password)
#         if user is not None:

#             login(request, user)

#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")

#         else:
#             # Return an 'invalid login' error message.
#             print("Error")

#     return render(request, "main/login.html", context)

class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'main/login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)


class MainView(View):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):
        tag_views = None
        property = None
        top_tags = None
        try:
            tag_views = request.user.tagview_set.all().order_by("-count")[:5]
        except:
            pass

        owned = None

        try:
            owned = request.user.myproperty.property.all()
        except:
            pass

        if tag_views:
            top_tags = [x.tag for x in tag_views]
            property = Property.objects.filter(tag__in=top_tags)
            if owned:
                property = property.exclude(pk__in=owned)

            if property.count() < 10:
                property = Property.objects.all().order_by("?")
                if owned:
                    property = Property.exclude(pk__in=owned)
                property = property[:10]
            else:
                property = property.distinct()
                property = sorted(property, key=lambda x: random.random())

        featured_property = list(Property.objects.filter(featured = True))
        shuffle(featured_property)
        # city          = City.objects.filter(slug__in = ["abuja" , "lagos" , "ibadan" , "calabar" , "kano","port-harcourt"]).order_by("id")
        featured_cities          = City.objects.filter(slug__in = ["abuja" , "lagos" , "ibadan" , "calabar" , "kano","port-harcourt"]).annotate(num_property = Count("property")).order_by("-num_property")

        cities = City.objects.all().annotate(num_property = Count("property")).order_by("-num_property")

        context = {
            "property": property,
            "top_tags": top_tags,
            "featured_property":featured_property,
            "featured_cities":featured_cities,
            "cities" : cities
        }
        return render(request, "main/index.html", context)

class ContactView(TemplateView):
    template_name = 'main/contact.html'

class AboutView(TemplateView):
    template_name = 'main/about.html'