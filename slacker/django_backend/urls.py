from django.conf.urls.defaults import *

from slacker.django_backend.views import slacker_execute

urlpatterns = patterns('',
    url(r'^execute/$', slacker_execute, name='slacker-execute'),
)
