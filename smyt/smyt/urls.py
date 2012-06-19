from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dynmodels.views import HomeView, list_models, model_data

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smyt.views.home', name='home'),
    # url(r'^smyt/', include('smyt.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^models/$', list_models, name='get_models'),
    url(r'^modeldata/$', model_data, name='model_data'),
)
