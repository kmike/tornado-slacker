from django.conf.urls.defaults import *

from async_orm.incarnations.http.views import orm_execute

urlpatterns = patterns('',
    url(r'^execute/$', orm_execute, name='async-orm-execute'),
)
