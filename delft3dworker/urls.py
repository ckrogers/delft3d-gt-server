from django.conf.urls import include, url, handler404, handler500  # noqa
from delft3dworker.views import runs
from delft3dworker.views import createrun
from delft3dworker.views import deleterun
from delft3dworker.views import celerytest

urlpatterns = (
    # Examples:
    url(r'^runs/$', runs, name='runs'),
    url(r'^createrun/$', createrun, name='createrun'),
    url(r'^deleterun/$', deleterun, name='deleterun'),

    url(r'^celerytest/$', celerytest, name='celerytest'),
)