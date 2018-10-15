from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from .import views
from django.contrib.auth.views import login,logout
# from main.views import IndexView, LoginView
from main.views import MainView, LoginView

from django.contrib.auth.views import(
    login,
    logout,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
    LogoutView,

    
)

from property.views import UserFavoriteProperty
from .views import ContactView, AboutView



app_name = 'main'




urlpatterns = [
    url(r'^$', MainView.as_view(), name='index'),
    
    # url(r'^login/$',login,{'template_name':'main/login.html'},name='login'),
    
    url(r'^contact/$',ContactView.as_view(),name='contact'),
    url(r'^about/$',AboutView.as_view(),name='about'),

    url(r'^login/$',LoginView.as_view(),name='login'),

    # url(r'^login/$',views.login_page,name='login'),

    # url(r'^logout/$',logout,{'template_name':'main/index.html'},name='logout'),

    url(r'^logout/$',LogoutView.as_view(),name='logout'),

    url(r'^register/$', views.register, name='register'),

    url(r'^change-password/$',views.change_password, name="change_password"),
   
    url(r'^profile/$',views.user_profile, name="profile"),
    
    url(r'^reset-password/$', password_reset, {'template_name':'main/reset_password.html',
                                                    'email_template_name':'main/reset_password_email.html',
                                                    'post_reset_redirect':'main:password_reset_done',
                                                    'from_email':'main@django.com',},name='password_reset'),

   
    url(r'^reset-password/done/$', password_reset_done, {'template_name': 'main/reset_password_done.html'},
                                                         name='password_reset_done'),

    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    password_reset_confirm, {'template_name':'main/reset_password_confirm.html',
                              'post_reset_redirect': reverse_lazy('main:password_reset_complete')},
                              name='password_reset_confirm'),

    url(r'reset-password/complete/$', password_reset_complete,{'template_name':'main/reset_password_complete.html'}, name='password_reset_complete'),

    url(r'^favorite/$',UserFavoriteProperty.as_view(),name='favorite'),

]


