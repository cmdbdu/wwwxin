from django.conf.urls import patterns, include, url


urlpatterns = patterns('authorized.views',
    url(r'^', 'index'),
)
