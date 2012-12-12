from django.conf.urls import patterns, include, url
from django.contrib.auth.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    url(r'^logout/$', 'app.views.logout', name='logout'),
    url(r'^login/$', 'app.views.login', name='login'),
    url(r'^register/$', 'app.views.register', name='register'),
    url(r'^ask/$', 'app.views.ask', name='ask'),
    url(r'^answer/$', 'app.views.answer', name='answer'),
    url(r'^question/(?P<question_id>\d+)/$', 'app.views.question', name='question'),
    url(r'^user/(?P<user_id>\d+)/$', 'app.views.user', name='user'),
    url(r'^edit_user/(?P<user_id>\d+)/$', 'app.views.edit_user', name='edit_user')
    # url(r'^queueoverflow/', include('queueoverflow.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
