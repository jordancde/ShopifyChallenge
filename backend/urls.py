from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

from django.urls import path, include
from django.contrib import admin
from django.conf.urls import include, url

from django.views.decorators.csrf import csrf_exempt

from backend import settings

from shopnet.auth import PrivateGraphQLView
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^logout/$', auth_views.logout, {'next_page': '/graphql'}, name='logout'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^graphql', PrivateGraphQLView.as_view(graphiql=True))
]
urlpatterns = format_suffix_patterns(urlpatterns)
