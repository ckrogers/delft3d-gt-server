from django.conf.urls import include, url, handler404, handler500  # noqa
from django.contrib.auth.decorators import login_required
from django.views.static import serve

from rest_framework import routers

from delft3dworker import views


# REST Framework Router

router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet, 'group')
router.register(r'scenarios', views.ScenarioViewSet, 'scenario')
router.register(r'scenes', views.SceneViewSet, 'scene')
router.register(r'templates', views.TemplateViewSet, 'template')
router.register(r'users', views.UserViewSet, 'user')

# url patterns

urlpatterns = (

    # REST Framework
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),

    # DATA
    url(r'^data(?P<path>.*)$', login_required(serve), {
        'document_root': '/data/',
    }),
    )
