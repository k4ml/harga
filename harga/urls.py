from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from haystack.query import SearchQuerySet
from haystack.views import search_view_factory

from harga.views import ProductSearchView, tmp_result

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

search_sqs = SearchQuerySet().order_by('-tarikh')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^myproject/', include('myproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'%s' % settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^soalan-lazim/$', 'harga.views.faq'),
    url(r'^tmp_result/', tmp_result),
    url(r'^search/', include('haystack.urls'), name='haystack-search'),
    url(r'', search_view_factory(
                view_class=ProductSearchView,
                searchqueryset=search_sqs
            ), name='search'),
)
