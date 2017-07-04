from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from mailer import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', login_required(views.SendMailFormView.as_view(), redirect_field_name=None), name='index'),
    url(r'^accounts/login/$', views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', views.logout_view, name='logout'),
    url(r'^accounts/register/$', views.SignUpView.as_view(), name='register'),
    url(r'^admin/', admin.site.urls),
]
