from django.conf.urls import url
from first_app import views

app_name = 'first_app'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'manage_subscriptions$', views.manage_subscriptions, name='manage_subscriptions'),
    url(r'make_query$', views.make_query, name='make_query'),
    url(r'results', views.results, name='results'),
    url(r'help$', views.help, name='help'),
]
