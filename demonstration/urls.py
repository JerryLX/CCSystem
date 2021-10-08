from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'runenv', views.runenv),
    url(r'show_progress', views.show_progress),
]