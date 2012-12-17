from django.conf.urls import patterns, include, url
from django.contrib.auth.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Home
    url(r'^$', 'app.views.home', name='home'),
    url(r'^sort/(?P<sort>\w+)$', 'app.views.home', name='home'),

    # Login
    url(r'^logout/$', 'app.views.logout', name='logout'),
    url(r'^login/$', 'app.views.login', name='login'),
    url(r'^register/$', 'app.views.register', name='register'),

    # Question/Answer
    url(r'^ask/$', 'app.views.ask', name='ask'),
    url(r'^answer/$', 'app.views.answer', name='answer'),
    url(r'^question/(?P<question_id>\d+)/$', 'app.views.question', name='question'),
    url(r'^edit_question/(?P<question_id>\d+)/$', 'app.views.edit_question', name='edit_question'),

    # User
    url(r'^user/(?P<user_id>\d+)/$', 'app.views.user', name='user'),
    url(r'^edit_user/(?P<user_id>\d+)/$', 'app.views.edit_user', name='edit_user'),

    # Votes
    url(r'^vote/(?P<vote_type>\d)/(?P<vote_value>.+)/(?P<item_id>\d+)/$', 'app.views.vote', name='vote'),
    url(r'^vote/$', 'app.views.vote', name='vote'),

    # Tags/Badges
    url(r'^tags/$', 'app.views.tags', name='tags'),
    url(r'^tag/(?P<tag_id>\d+)/$', 'app.views.tag', name='tag'),
    url(r'^badge/(?P<badge_id>\d+)/$', 'app.views.badge', name='badge'),
    url(r'^badges/$', 'app.views.badges', name='badges'),

    # Account Mnagement
    url(r'^reset_password/$', 'app.views.reset_password', name='reset_password'),
    url(r'^reset_password/(?P<reset_id>\w+)/$', 'app.views.reset_password', name='reset_password'),
    url(r'^activate_user/(?P<activate_id>\w+)/$', 'app.views.activate_user', name='activate_user'),
    url(r'^activate_user/$', 'app.views.activate_user', name='activate_user'),
    url(r'^deactivate_user/(?P<user_id>\d+)/$', 'app.views.deactivate_user', name='deactivate_user'),


    # url(r'^queueoverflow/', include('queueoverflow.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
